# TIMES-NZ Excel files

Version: 3.0.8

This repository houses release versions of TIMES-NZ Excel configuration data files. These fully define all optional input components of TIMES-NZ model scenarios, but do not include results or raw data. They are intended for use by modellers, developers, or students who wish to work with the TIMES-NZ model without needing to perform preprocessing.

We recommend Veda Online for working with these files. If you wish to inspect the model in more detail, full data, code, and assumptions documentation are available at the [TIMES-NZ repository](https://github.com/EECA-NZ/TIMES-NZ-Model-Files). 

## Quickstart guide

This guide should enable users to run TIMES-NZ solves, recreate existing results, and build their own sensitivities by changing selected scenario components. Full Veda Online feature documentation is available [here](https://kanors-emr.github.io/VedaOnline-documentation/). 

**1. Creating the model**

Visit [Veda Online](https://vedaonline.cloud/), and create an account. Select "Create Model", and in the github repository simply enter this repository's address:

```
https://github.com/EECA-NZ/TIMES-NZ-Excel-Files.git
```
Under branch, select "main", then click "Clone". Other versions of the model may be available here in future. Note that Veda Online requires a license for longterm use, but a free week trial is available. This quickstart guide should now also be visible in the About section. 

**2. Synchronise the data**

Head to the *Navigator* tab, ensure all files are selected, and click "Synchronise". This converts the excel files to TIMES-compatible files to prepare for solving. 

See [here](https://kanors-emr.github.io/VedaOnline-documentation/model_workspace/Navigator/) for current VO documentation on the Navigator tab's features. 

The current model database is viewable in the Items View and Browse windows.

**3. Solve a case**

The *Run Manager* tab enables the users to define and solve "cases", which are selected combinations of model components that define a scenario. TIMES-NZ cases developed by EECA's modelling team are available. In the *Manage Saved Cases* window, you can select and solve cases already defined by the TIMES-NZ development team. For example, select "steady-V308" and "shift-v308", then click "Solve" for the solver to produce results for these. 

Scenario sensitivities are also available, and it's possible to build your own (see below).

**4. Investigate results**

The *Results* tab will provide all results, but they are difficult to interpret as they only contain item codes, which are not designed to be human-readable. Instead, in the *Reports* tab, you can select variables and categories to build your own charts to inspect results or compare scenarios. 

Note that all concordance files, which map TIMES-NZ codes to human-readable categories, are also included in this repository under `concordances`. It is possible to download raw result tables from the *Results* window, then use these files to create your own datasets as desired. 

(This step needs further testing and might need more detail)

**5. Create your own scenarios**

The Cases defined in the *Run Manager* tab include "Scenario Groups", which define which combinations of input files are combined within the scenario. Currently, all available cases include distinct Scenario Groups, including our sensitivity case scenarios. 

It is easy to create a new Scenario Group by changing the combinations of selected data. For example, you might wish to run the Steady scenario, but modified to include the higher carbon prices of the Shift scenario. Simply select the Steady scenario group, modify it to remove `Carbon_Steady` and instead include `Carbon_Shift`, and save your new Scenario Group. Then, create a case that uses this Scenario Group, with a name of your choosing, and solve this case. Now, your new results are available in the *Reports* tab to compare to other results.


**6. Modify input data**

It is more involved to modify the underlying data further, but this is also possible. You will need to create a new repository to make your own adjustments to the source files. Feel free to fork this repository, make changes as you see fit, and create a new Veda Online model that instead uses your forked repository. Depending on the complexity of the changes you wish to introduce, you may wish to also reference TIMES documentation files, which are available [here](https://github.com/etsap-TIMES/TIMES_Documentation). 

## Digging deeper 

More advanced users may also be interested in the [TIMES-NZ source repo](https://github.com/EECA-NZ/TIMES-NZ-Model-Files). This repo includes all raw data, assumptions, and code used to create TIMES-NZ model, not only the input files found here. If there are any version mismatches, the source repo should be considered the source of truth. 





