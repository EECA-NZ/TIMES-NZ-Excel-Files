# TIMES-NZ for Veda Online

Version: 3.0.8


This repository houses release versions of TIMES-NZ Excel configuration data files. These fully define all optional input components of TIMES-NZ model scenarios, but do not include results or raw data. They are intended for use by modellers, developers, or students who wish to work with the TIMES-NZ model without needing to perform preprocessing.

We recommend Veda Online for working with these files. 

Full data, code, and assumptions documentation for TIMES-NZ 3.0 are available at the [TIMES-NZ source repository](https://github.com/EECA-NZ/TIMES-NZ-Model-Files). 

## Quickstart guide

This guide should enable users to run TIMES-NZ solves, recreate existing results, and build their own sensitivities by changing selected scenario components. Full Veda Online feature documentation is available [here](https://kanors-emr.github.io/VedaOnline-documentation/). 

**1. Creating the model**

Visit [Veda Online](https://vedaonline.cloud/), and create an account. Select "Create Model", and in the github repository simply enter this repository's address:

```
https://github.com/EECA-NZ/TIMES-NZ-Excel-Files.git
```
Under branch, select "main", then click "Clone". Other versions of the model may be available here in future. You can now view this quickstart guide in the model's *About* section.

Note that Veda Online requires a license for longterm use, but a free week trial is available.

**2. Synchronise the data**

Head to the *Navigator* tab, ensure all files are selected, and click "Synchronise". This converts the excel files to TIMES-compatible files to prepare for solving. It can take a small moment to get started, so don't worry if it doesn't look like anything is happening at first. 

See [here](https://kanors-emr.github.io/VedaOnline-documentation/model_workspace/Navigator/) for more detail current VO documentation on the Navigator tab's features. After synchronisation, the current model database is also viewable in the *Items View* and *Browse* tabs.

**3. Solve a case**

The *Run Manager* tab enables the users to define and solve "cases", which are selected combinations of model components that define a scenario. TIMES-NZ cases developed by EECA's modelling team are available. In the *Manage Saved Cases* window, you can select and solve cases already defined by the TIMES-NZ development team. For example, select "steady-V308" and "shift-v308", then click "Solve" for the solver to produce results for these. 

Scenario sensitivities are also available, and it's possible to build your own (see below).

**4. Investigate results**

You can use the *Reports* tab to investigate results with our post-processing labels. This makes results possible to interpret, but there are a few steps involved in ensuring that the outputs are sensible.



1. Go to the *Reports* tab, which should show options for the key dimensions (Scenario, Region, Variable, and Year), and a selection of additional dimensions. 
2. Select at least one variable. Current options include electricity generation, emissions, final energy demand, or final energy demand by timeslice. Select "Get Data".
3. This brings you to the report page, which renders a table by default. It's possible to instead create a range of charts from the dropdown menu.
4. This report page uses "Process" and "Commodity" codes by default for grouping the results. These are internal model codes, and difficult to make sense of. It is recommended that users adjust these by dragging other grouping variables from the bottom to the top left of the chart. Using grouping categories like "Fuel" or "Sector" are likely to be much more useful for analysis.

(Note that the *Results* tab only includes raw results, which can be useful for debugging but is not recommended for analysis)


We encourage you to explore the results of our scenarios, or those you create yourself. There are a range of additional features in the report viewer, and you can read about those in more detail [here](https://kanors-emr.github.io/VedaOnline-documentation/model_workspace/Reports/).



```{note}
Note: the LMADefs_TIMESNZ.xlsx file is used to label raw data.

It is built from the TIMES-NZ concordance tables, which are also available in `concordances/` if you wish to explore these further.
```

**5. Create your own scenarios**

The Cases defined in the *Run Manager* tab include "Scenario Groups", which define which combinations of input files are used to create the scenario. Currently, all available cases include distinct Scenario Groups, including our sensitivity case scenarios. 

It is straightforward to create a new Scenario Group by changing the combinations of selected data. For example, you might wish to run the Steady scenario, but modified to include the higher carbon prices of the Shift scenario. Simply select the Steady scenario group, modify it to remove `Carbon_Steady` and instead include `Carbon_Shift`, and save your new Scenario Group. Then, create a case that uses this Scenario Group, with a name of your choosing, and solve this case. Now, your new results are available in the *Reports* tab to compare to other results.

The below tables lists files that may be useful to mix and match or remove from scenarios to produce different outcomes. Most have different options linked to either the `Steady` or `Shift` scenario, but some files are standalone and may be associated with both, or only one.

| External projection scenario files  | What it changes |
| --- | --- |
| `Carbon_[SCENARIO].xlsx` | Carbon-price projections. |
| `ScenDem_[SCENARIO].xlsx` | Demand projections. |
| `DistributedSolar_[SCENARIO].xlsx` | Distributed-solar uptake projections. |
| `NewTechDemand.xlsx` | Additional demand from "new technologies" in the Shift scenario. |

| Future technologies and their costs | What it changes |
| --- | --- |
| `NewTechs_AGR_[SCENARIO].xlsx` | Agriculture demand technologies and costs |
| `NewTechs_COM.xlsx` | Commercial technologies and costs |
| `NewTechs_ELC_[SCENARIO].xlsx` | Future electricity generation plants and costs |
| `NewTechs_H2_[SCENARIO].xlsx` | Future hydrogen electrolyser costs |
| `NewTechs_TRA_[SCENARIO].xlsx` | Future transport vehicle costs and efficiencies |
| `NewTech_Storage_[SCENARIO].xlsx` | Future battery costs |
| `DemandFlex_[SCENARIO].xlsx` | Demand-flexibility option availability. |


| Other components | What it changes |
| --- | --- |
| `DiscountRates_[SCENARIO].xlsx` | Discount rates used in the scenario |
| `LNG_Imports.xlsx` | LNG-import option availability, used in Steady. |
| `AdditionalBioenergySupply.xlsx` | Additional bioenergy supply used for Shift. |
| `ProcessHeatCoalBan.xlsx` | Coal-use restrictions for process heat. |
| `WEM_WCM.xlsx` | Winter energy margin and peak constraints. |



**6. Modify input data**

It is more involved to modify the underlying data further, but this is also possible. You will need to create a new repository to make your own adjustments to the source files. Feel free to fork this repository, make changes as you see fit, and create a new Veda Online model that instead uses your forked repository. Depending on the complexity of the changes you wish to introduce, you may wish to also reference TIMES documentation files, which are available [here](https://github.com/etsap-TIMES/TIMES_Documentation). 

## Digging deeper 

More advanced users may also be interested in the [TIMES-NZ source repo](https://github.com/EECA-NZ/TIMES-NZ-Model-Files). This repo includes all raw data, assumptions, and code used to create TIMES-NZ model, not only the input files found here. If there are any version mismatches, the source repo should be considered the source of truth. 

## Contact 

Please contact times-nz@eeca.govt.nz with any feedback, questions, or comments. 





