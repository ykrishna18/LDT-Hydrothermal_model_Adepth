#!/usr/bin/env python3

import os
import re
import csv

# ------------------------------------------------------------
# SETTINGS
# ------------------------------------------------------------

case_dir = "."          # Run script from OpenFOAM case directory
patch_name = "top"
field_name = "phi"

SECONDS_PER_YEAR = 365.25 * 24 * 3600

output_file = "top_mass_flux.csv"


# ------------------------------------------------------------
# READ phi VALUES ON A PATCH
# ------------------------------------------------------------

def read_patch_values(phi_file, patch_name):
    """
    Reads the nonuniform scalar values of a boundary patch
    from an OpenFOAM surfaceScalarField file.
    """

    with open(phi_file, "r") as f:
        text = f.read()

    # Find boundaryField section
    boundary_pos = text.find("boundaryField")

    if boundary_pos == -1:
        raise ValueError("boundaryField not found")

    boundary_text = text[boundary_pos:]

    # Find the requested patch
    patch_pattern = re.compile(
        r"\b" + re.escape(patch_name) + r"\b\s*\{",
        re.MULTILINE
    )

    match = patch_pattern.search(boundary_text)

    if not match:
        raise ValueError(f"Patch '{patch_name}' not found")

    patch_start = match.end()

    # Find matching closing brace of patch
    depth = 1
    i = patch_start

    while i < len(boundary_text) and depth > 0:

        if boundary_text[i] == "{":
            depth += 1

        elif boundary_text[i] == "}":
            depth -= 1

        i += 1

    patch_text = boundary_text[patch_start:i-1]

    # --------------------------------------------------------
    # Look for:
    #
    # value nonuniform List<scalar>
    # 80
    # (
    # ...
    # );
    # --------------------------------------------------------

    pattern = re.compile(
        r"value\s+nonuniform\s+List<scalar>\s*"
        r"(\d+)\s*"
        r"\(\s*"
        r"(.*?)"
        r"\s*\)\s*;",
        re.DOTALL
    )

    value_match = pattern.search(patch_text)

    if not value_match:

        # Sometimes phi may be stored simply as nonuniform
        pattern2 = re.compile(
            r"nonuniform\s+List<scalar>\s*"
            r"(\d+)\s*"
            r"\(\s*"
            r"(.*?)"
            r"\s*\)\s*;",
            re.DOTALL
        )

        value_match = pattern2.search(patch_text)

    if not value_match:
        raise ValueError(
            f"No nonuniform List<scalar> found for patch '{patch_name}'"
        )

    expected_count = int(value_match.group(1))

    value_text = value_match.group(2)

    values = [
        float(x)
        for x in re.findall(
            r"[-+]?(?:\d*\.\d+|\d+\.?)(?:[eE][-+]?\d+)?",
            value_text
        )
    ]

    if len(values) != expected_count:
        raise ValueError(
            f"Expected {expected_count} values but found {len(values)}"
        )

    return values


# ------------------------------------------------------------
# FIND ALL OPENFOAM TIME DIRECTORIES
# ------------------------------------------------------------

time_dirs = []

for item in os.listdir(case_dir):

    full_path = os.path.join(case_dir, item)

    if not os.path.isdir(full_path):
        continue

    try:
        time_value = float(item)
        time_dirs.append((time_value, item))

    except ValueError:
        pass


time_dirs.sort(key=lambda x: x[0])


# ------------------------------------------------------------
# PROCESS EACH TIME
# ------------------------------------------------------------

results = []

print()
print("Processing top mass flux")
print("-" * 75)

for time_seconds, dirname in time_dirs:

    phi_file = os.path.join(case_dir, dirname, field_name)

    if not os.path.isfile(phi_file):
        print(f"Skipping {dirname}: phi not found")
        continue

    try:

        phi = read_patch_values(phi_file, patch_name)

        # ----------------------------------------------------
        # OpenFOAM convention:
        # positive phi = outward through boundary
        # negative phi = inward through boundary
        # ----------------------------------------------------

        positive_faces = [p for p in phi if p > 0]
        negative_faces = [p for p in phi if p < 0]

        # Hydrothermal discharge
        outflow = sum(positive_faces)

        # Recharge reported as positive magnitude
        recharge = -sum(negative_faces)

        # Signed net flux
        net_flux = sum(phi)

        time_years = time_seconds / SECONDS_PER_YEAR

        results.append([
            time_seconds,
            time_years,
            outflow,
            recharge,
            net_flux,
            len(positive_faces),
            len(negative_faces)
        ])

        print(
            f"{time_years:8.2f} yr   "
            f"out = {outflow:12.6e}   "
            f"in = {recharge:12.6e}   "
            f"net = {net_flux:12.6e}"
        )

    except Exception as e:

        print(f"ERROR at time {dirname}: {e}")


# ------------------------------------------------------------
# WRITE CSV
# ------------------------------------------------------------

with open(output_file, "w", newline="") as f:

    writer = csv.writer(f)

    writer.writerow([
        "Time_s",
        "Time_years",
        "Outflow_kg_s",
        "Recharge_kg_s",
        "NetFlux_kg_s",
        "Number_outflow_faces",
        "Number_recharge_faces"
    ])

    writer.writerows(results)


print()
print("-" * 75)
print(f"Saved: {output_file}")
print()
