# TIMES-NZ Excel files

This repository houses release versions of TIMES-NZ Excel configuration data files. These fully define all optional input components of TIMES-NZ model scenarios, but do not include results or raw data. They are intended for use by modellers, developers, or students to enable working with the TIMES-NZ model without needing to perform preprocessing locally. 

The [TIMES-NZ source repo](https://github.com/EECA-NZ/TIMES-NZ-Model-Files) includes all raw data, assumptions, and code used to create these configuration files. If there are any version mismatches, the source repo should be considered the source of truth. 


## Supporting resources

These files are challening to interpret in isolation. The following resources provide useful context: 

- [Documentation for the TIMES Model Part IV: Veda 2.0](https://github.com/etsap-TIMES/TIMES_Documentation/blob/master/Documentation_for_the_TIMES_Model-Part-IV.pdf) describes how attributes and data are declared for a TIMES model in Veda. Technical definitions of the variables and structures are defined here. 

- The [TIMES-NZ documentation site](https://times-nz-docs.readthedocs.io/en/latest) fully describes input data and methods used to create these files. 

Users may also find the [process and commodity](https://times-nz-docs.readthedocs.io/en/latest/developer_guide/code-lookups.html) lookup code tables useful for adding meaning to internal model codes. These are intended to be used in interpreting output files, and were used to create the [TIMES-NZ data explorer](https://www.eeca.govt.nz/insights/data-tools/new-zealand-energy-scenarios-times-nz/). 

From major version 3 onwards, the accompanying `metadata.csv` file describes each tagged table and its location within the Excel workbook structure. This can assist developers in identifying specific inputs and their context within the wider structure

## Recommended use

These files contain the model input data and optional model components. To run the model, users must define a scenario, process the input data into TIMES/GAMS run files, and solve the resulting optimisation problem. This workflow is commonly managed using Veda, but alternative approaches are available, such as the [xl2times utility](https://github.com/etsap-TIMES/xl2times). 

Scenario definitions (or "cases") can be configured within Veda, and define which model components are selected for a particular scenario. Case files used for TIMES-NZ release scenarios (including *Steady*, *Shift*, and related sensitivities) are included. 

Users without a Veda licence may wish to use a [Veda Online](https://vedaonline.cloud/) trial account for modest test runs. A model can be created by cloning this public repository as its data source. The trial is limited in duration and available solve time; see the [Veda Online documentation](https://vedaonline-documentation.readthedocs.io/en/latest/) for current details.

If you wish to modify the input files for your own model or scenarios, we recommend forking this repository and making changes in your fork. Advanced users may also wish to fork the source repository and modify the preprocessing code directly.




