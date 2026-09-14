# Conceptual numerical models of hydrothermal circulation at the Lava–Dyke Transition

This repository contains the numerical models and post-processing
scripts associated with the Lava–Dyke Transition (LDT) modelling
section of:

"TITLE OF MANUSCRIPT"

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

cases/            OpenFOAM model configurations
postprocessing/   Python analysis scripts
data/             Processed data used for manuscript figures/tables
figures/          Figures generated from the model results
docs/             Additional model documentation

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
