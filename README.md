# Conceptual numerical models of hydrothermal circulation at the Lava–Dyke Transition

This repository contains the numerical models and post-processing
scripts associated with the Lava–Dyke Transition (LDT) modelling
section of:

"Sulphides are everywhere"

## Purpose

The simulations are simplified conceptual experiments designed to
investigate how dyke emplacement and crustal permeability structure
influence hydrothermal circulation within the LDT.

The models are not intended as site-specific reconstructions or
reactive-transport simulations of sulphide precipitation.

## Model cases

### Case 1 – Long dyke
Three dyke intrusions are represented, with the central intrusion
extending farther toward the seafloor.

### Case 2 – Short dyke
Similar crustal architecture to Case 1, but with a reduced vertical
extent of the central dyke.

### Case 3 – Dyke + fault
A high-permeability fault is introduced adjacent to the dyke to
investigate its influence on hydrothermal recharge and subsurface
fluid circulation.

## Numerical model

Simulations were performed using OpenFOAM and the HTFoam
hydrothermal fluid-flow solver.

Detailed model parameters and boundary conditions are provided in
the manuscript Supplementary Information.

## Repository structure

```text
LDT-Hydrothermal_model_Adepth/
│
├── Case_1/
│   ├── 0/                         # Initial and boundary conditions
│   ├── constant/                  # Physical and thermophysical properties
│   ├── system/                    # Mesh, solver, and numerical settings
│   ├── Case1_3.png                # Temperature field at 3 years
│   ├── Case1_6.png                # Temperature field at 6 years
│   ├── Case1_100.png              # Temperature field at 100 years
│   ├── clean.sh                   # Case cleaning script
│   ├── run.sh                     # Serial run script
│   ├── run_par.sh                 # Parallel run script
│   ├── sulphide_fluX_calculation.py
│   └── ventT.txt
│
├── case_2/
│   ├── 0/
│   ├── constant/
│   ├── system/
│   ├── ...
│   └── sulphide_fluX_calculation.py
│
├── Case_3/
│   ├── 0/
│   ├── constant/
│   ├── system/
│   ├── ...
│   └── sulphide_fluX_calculation.py
│
└── README.md
```

### Model cases

The repository contains three simplified two-dimensional numerical
experiments designed to investigate the influence of dyke geometry
and fault-controlled permeability on hydrothermal circulation within
the lava–dyke transition (LDT).

**Case 1 – Extended dyke intrusion**

Case 1 represents a dyke configuration in which the central dyke
extends farther upward through the crust. The configuration is used
to investigate the effect of greater vertical dyke extent on
high-temperature hydrothermal discharge toward the seafloor.

**Case 2 – Shorter dyke intrusion**

Case 2 represents a similar crustal configuration but with a shorter
central dyke intrusion. Comparison between Cases 1 and 2 is used to
evaluate how the vertical extent of dyke emplacement influences the
thermal perturbation and the flux of high-temperature (>350 °C)
hydrothermal fluid across the upper boundary.

**Case 3 – Dyke–fault interaction**

Case 3 introduces a high-permeability fault in proximity to the dyke
system. The model is used to investigate how fault-controlled
seawater recharge modifies dyke-driven hydrothermal circulation and
the distribution of high-temperature fluids at depth.

### OpenFOAM case directories

Each model case contains the standard OpenFOAM case structure:

- `0/` – initial and boundary conditions for temperature, pressure,
  permeability, and other model fields.
- `constant/` – gravitational acceleration, transport properties,
  thermophysical properties, and xThermo configuration.
- `system/` – mesh generation, field initialization, numerical
  schemes, solver controls, decomposition settings, and other
  OpenFOAM configuration files.

The simulation output time directories and decomposed `processor*`
directories are not included in the repository.

### Post-processing

The Python post-processing scripts calculate the discharge of
high-temperature hydrothermal fluid and provide first-order estimates
of potential H2S deposition.

High-temperature discharge is defined as outward hydrothermal flow
across the upper model boundary with fluid temperatures exceeding
350 °C.

The H2S calculations use the concentration range and assumed
depositional efficiencies described in the associated manuscript.
These calculations are intended as first-order estimates and do not
represent explicit reactive-transport modelling of sulphide
precipitation.

### Model snapshots

Representative temperature fields are provided for selected
simulation times to illustrate the transient thermal evolution of
each model configuration. The complete numerical output is not
included because of its size.

## High-temperature discharge

High-temperature hydrothermal discharge is defined using fluid
discharging through the upper boundary at temperatures >350 °C.

## H2S deposition estimates

H2S deposition was estimated from the calculated high-temperature
fluid discharge using H2S concentrations of 27–85 ppm and the
deposition efficiencies described in the manuscript.

These calculations represent first-order estimates and do not
constitute explicit reactive-transport modelling of sulphide
precipitation.

## Software

- OpenFOAM 10
- HTFoam
- xThermo
- Python 3
HTFoam and xThermo are external dependencies and are not distributed
as part of this repository.
