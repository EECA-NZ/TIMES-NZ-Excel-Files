#!/usr/bin/env python3
"""Build the report-definition workbook from the model concordances."""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "LMADefs_TIMESNZ.xlsx"
NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKGREL = "http://schemas.openxmlformats.org/package/2006/relationships"

# Veda adds one report-table column for every distinct `_Map.dimension`.
# Commodity sector and end-use classifications are kept distinct from their
# process counterparts because they describe different things.
PROCESS_DIMENSION_NAMES = {}
COMMODITY_DIMENSION_NAMES = {
    "Sector": "Commodity_Sector",
    "SectorGroup": "Commodity_SectorGroup",
    "EndUse": "Commodity_EndUse",
}


def csv_rows(directory: Path):
    for path in sorted(directory.glob("*.csv")):
        with path.open(encoding="utf-8-sig", newline="") as handle:
            yield path.name, list(csv.DictReader(handle))


def process_maps():
    mapped = set()
    rows = []
    for _, source_rows in csv_rows(ROOT / "concordances/processes"):
        for source in source_rows:
            process = source.get("Process")
            if not process:
                continue
            for dimension, value in source.items():
                # Commodity links describe process topology rather than an
                # independent reporting dimension.  In particular, shared
                # electrified demand technologies can have several outputs.
                if dimension in {
                    "Process", "Commodity", "CommodityOut", "sets", "tact",
                    "tcap", "Description", "Imported", "Note", "Fuel",
                    "FuelDetail", "FuelGroup", "Renewable",
                } or not value:
                    continue
                report_dimension = PROCESS_DIMENSION_NAMES.get(dimension, dimension)
                key = (report_dimension, value, process)
                if key not in mapped:
                    mapped.add(key)
                    # The optional `name` pattern is deliberately omitted:
                    # pset_pn is the actual process filter.  Including a
                    # wholly blank `name` column causes Veda Online to
                    # materialise duplicate `name` fields in pilot_runs.
                    rows.append([report_dimension, value, process])
    return sorted(rows, key=lambda r: (r[0], r[1], r[2]))


def commodity_maps():
    mapped = set()
    rows = []
    for _, source_rows in csv_rows(ROOT / "concordances/commodities"):
        for source in source_rows:
            commodity = source.get("Commodity")
            if not commodity:
                continue
            for dimension, value in source.items():
                if dimension in {
                    "Commodity", "csets", "unit", "Description", "SectorGroup",
                } or not value:
                    continue
                report_dimension = COMMODITY_DIMENSION_NAMES.get(dimension, dimension)
                key = (report_dimension, value, commodity)
                if key not in mapped:
                    mapped.add(key)
                    # As above, match through cset_cn and omit the unused
                    # `name` pattern column.
                    rows.append([report_dimension, value, commodity])
    return sorted(rows, key=lambda r: (r[0], r[1], r[2]))


def model_sets():
    psets = set()
    csets = set()
    for _, rows in csv_rows(ROOT / "concordances/processes"):
        for row in rows:
            psets.update(v.strip() for v in row.get("sets", "").split(",") if v.strip())
    for _, rows in csv_rows(ROOT / "concordances/commodities"):
        for row in rows:
            csets.update(v.strip() for v in row.get("csets", "").split(",") if v.strip())
    return sorted(psets), sorted(csets)


def col_name(number):
    result = ""
    while number:
        number, remainder = divmod(number - 1, 26)
        result = chr(65 + remainder) + result
    return result


def sheet_xml(rows):
    sheet = Element("{%s}worksheet" % NS)
    width = max(len(row) for row in rows)
    SubElement(sheet, "{%s}dimension" % NS, ref=f"A1:{col_name(width)}{len(rows)}")
    views = SubElement(sheet, "{%s}sheetViews" % NS)
    view = SubElement(views, "{%s}sheetView" % NS, workbookViewId="0")
    SubElement(view, "{%s}pane" % NS, ySplit="2", topLeftCell="A3", activePane="bottomLeft", state="frozen")
    cols = SubElement(sheet, "{%s}cols" % NS)
    for i in range(1, width + 1):
        SubElement(cols, "{%s}col" % NS, min=str(i), max=str(i), width="24", customWidth="1")
    data = SubElement(sheet, "{%s}sheetData" % NS)
    for ri, row in enumerate(rows, 1):
        row_el = SubElement(data, "{%s}row" % NS, r=str(ri))
        for ci, value in enumerate(row, 1):
            if value == "":
                continue
            cell = SubElement(row_el, "{%s}c" % NS, r=f"{col_name(ci)}{ri}", t="inlineStr")
            inline = SubElement(cell, "{%s}is" % NS)
            text = SubElement(inline, "{%s}t" % NS)
            text.text = str(value)
    SubElement(sheet, "{%s}pageMargins" % NS, left="0.7", right="0.7", top="0.75", bottom="0.75", header="0.3", footer="0.3")
    return tostring(sheet, encoding="utf-8", xml_declaration=True)


def build():
    psets, csets = model_sets()
    sheets = [
        ("TS_Defs", [
            ["~TS_Defs"],
            ["Attribute", "WAttribute", "Vintage", "PSET_Set", "PSET_PN", "PSET_PD", "PSET_CI", "PSET_CO", "CSET_Set", "CSET_CN", "CSET_CD", "Unit", "TS", "UC_N", "Name", "Desc", "Ldesc", "show_me", "Ignore"],
            # Leave WAttribute blank: it is solely for weighted-average
            # measures, not for selecting an energy or emissions commodity.
            ["VAR_FIN", "", "", "DMD", "", "", "", "", "NRG", "", "", "PJ", "", "", "Final_energy_demand", "Final energy demand", "Annual final energy demand", "p,c", ""],
            ["VAR_FIN", "", "", "DMD", "", "", "", "", "NRG", "", "", "PJ", "", "", "Final_energy_demand_timesliced", "Final energy demand by timeslice", "Final energy demand retaining TIMES timeslices", "p,c,t", ""],
            ["VAR_FOUT", "", "", "ELE", "-ELC_BAT_*", "", "", "", "NRG", "", "", "PJ", "", "", "Electricity_generation", "Electricity generation", "Electricity output from electricity-generation processes, excluding batteries", "p,c", ""],
            ["VAR_FOUT", "", "", "", "", "", "", "", "ENV", "-TOTCO2", "", "kt", "", "", "Emissions", "Emissions", "Process emissions, excluding the aggregate TOTCO2 commodity", "p,c", ""],
        ]),
        ("Process_Map", [["~Process_Map"], ["dimension", "description", "pset_pn"], *process_maps()]),
        ("Commodity_Map", [["~Commodity_Map"], ["dimension", "description", "cset_cn"], *commodity_maps()]),
        # Use the template's Veda headers exactly.  The concordances supply set
        # identifiers but no separate short/long descriptions, so retain the
        # identifier as the short description and leave the long one blank.
        ("PSet_Map", [["~PSet_Map"], ["Pset", "Desc", "Ldesc"], *[[value, value, ""] for value in psets]]),
        ("CSet_Map", [["~CSet_Map"], ["Cset", "Desc", "Ldesc"], *[[value, value, ""] for value in csets]]),
    ]
    with ZipFile(OUT, "w", ZIP_DEFLATED) as book:
        content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>''' + "".join(f'<Override PartName="/xl/worksheets/sheet{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>' for i in range(1, len(sheets) + 1)) + '''<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/></Types>'''
        book.writestr("[Content_Types].xml", content_types)
        book.writestr("_rels/.rels", f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="{PKGREL}"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>''')
        workbook = Element("{%s}workbook" % NS, {"xmlns:r": REL})
        sheets_el = SubElement(workbook, "{%s}sheets" % NS)
        for i, (name, _) in enumerate(sheets, 1):
            SubElement(sheets_el, "{%s}sheet" % NS, name=name, sheetId=str(i), **{"{%s}id" % REL: f"rId{i}"})
        book.writestr("xl/workbook.xml", tostring(workbook, encoding="utf-8", xml_declaration=True))
        relationships = "".join(f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{i}.xml"/>' for i in range(1, len(sheets) + 1))
        book.writestr("xl/_rels/workbook.xml.rels", f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="{PKGREL}">{relationships}<Relationship Id="rId{len(sheets)+1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>''')
        book.writestr("xl/styles.xml", f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><styleSheet xmlns="{NS}"><fonts count="1"><font><sz val="11"/><name val="Calibri"/></font></fonts><fills count="1"><fill><patternFill patternType="none"/></fill></fills><borders count="1"><border/></borders><cellStyleXfs count="1"><xf/></cellStyleXfs><cellXfs count="1"><xf xfId="0"/></cellXfs></styleSheet>''')
        for i, (_, rows) in enumerate(sheets, 1):
            book.writestr(f"xl/worksheets/sheet{i}.xml", sheet_xml(rows))
    print(f"Wrote {OUT.name}")


if __name__ == "__main__":
    build()
