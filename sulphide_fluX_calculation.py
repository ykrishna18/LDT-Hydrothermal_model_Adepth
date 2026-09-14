#!/usr/bin/env python3

import os
import re
import csv
import matplotlib.pyplot as plt
# ------------------------------------------------------------
# SETTINGS
# ------------------------------------------------------------

case_dir = "."
patch_name = "top"

phi_field = "phi"
T_field = "T"

SECONDS_PER_YEAR = 365.25 * 24 * 3600

output_file = "andersen_H2S_flux.csv"


# ------------------------------------------------------------
# ANDERSEN ET AL. SETTINGS
# ------------------------------------------------------------

# Only high-temperature fluids considered
T_CUTOFF_C = 350.0
T_CUTOFF_K = T_CUTOFF_C + 273.15

# H2S concentration range reported for Logatchev
H2S_LOW = 27e-6       # 27 ppm
H2S_HIGH = 85e-6      # 85 ppm

# Depositional efficiencies
EFF_LOW = 0.025
EFF_MID = 0.05
EFF_HIGH = 0.10


# ------------------------------------------------------------
# READ PATCH SCALAR VALUES
# ------------------------------------------------------------

def read_patch_values(field_file, patch_name):

    with open(field_file, "r") as f:
        text = f.read()

    boundary_pos = text.find("boundaryField")

    if boundary_pos == -1:
        raise ValueError("boundaryField not found")

    boundary_text = text[boundary_pos:]

    patch_pattern = re.compile(
        r"\b" + re.escape(patch_name) + r"\b\s*\{",
        re.MULTILINE
    )

    match = patch_pattern.search(boundary_text)

    if not match:
        raise ValueError(f"Patch '{patch_name}' not found")

    patch_start = match.end()

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
    # NONUNIFORM VALUES
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

    if value_match:

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
                f"Expected {expected_count} values "
                f"but found {len(values)}"
            )

        return values


    # --------------------------------------------------------
    # UNIFORM VALUE
    # --------------------------------------------------------

    uniform_pattern = re.compile(
        r"value\s+uniform\s+"
        r"([-+]?(?:\d*\.\d+|\d+\.?)(?:[eE][-+]?\d+)?)"
        r"\s*;"
    )

    uniform_match = uniform_pattern.search(patch_text)

    if uniform_match:
        return float(uniform_match.group(1))

    raise ValueError(
        f"No readable values found for patch '{patch_name}'"
    )


# ------------------------------------------------------------
# FIND TIME DIRECTORIES
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
# PROCESS TIME STEPS
# ------------------------------------------------------------

results = []

print()
print("Andersen H2S flux calculation")
print("-" * 120)

for time_seconds, dirname in time_dirs:

    phi_file = os.path.join(case_dir, dirname, phi_field)
    T_file = os.path.join(case_dir, dirname, T_field)

    if not os.path.isfile(phi_file):
        print(f"Skipping {dirname}: phi not found")
        continue

    if not os.path.isfile(T_file):
        print(f"Skipping {dirname}: T not found")
        continue

    try:

        phi = read_patch_values(phi_file, patch_name)
        T = read_patch_values(T_file, patch_name)

        if isinstance(phi, float):
            raise ValueError(
                "phi is uniform; individual outflow faces cannot be identified"
            )

        if isinstance(T, float):
            T = [T] * len(phi)

        if len(phi) != len(T):
            raise ValueError(
                f"phi has {len(phi)} faces but T has {len(T)} faces"
            )


        # ----------------------------------------------------
        # TOTAL AND HOT OUTFLOW
        # ----------------------------------------------------

        total_outflow = 0.0
        recharge = 0.0
        hot_outflow = 0.0

        outflow_faces = 0
        hot_faces = 0

        for phi_i, T_i in zip(phi, T):

            if phi_i > 0:

                total_outflow += phi_i
                outflow_faces += 1

                if T_i >= T_CUTOFF_K:

                    hot_outflow += phi_i
                    hot_faces += 1

            elif phi_i < 0:

                recharge += -phi_i


        net_flux = sum(phi)

        if total_outflow > 0:
            hot_fraction = hot_outflow / total_outflow
        else:
            hot_fraction = 0.0


        # ----------------------------------------------------
        # H2S FLUX
        # ----------------------------------------------------

        # kg H2S / s
        H2S_low_kg_s = hot_outflow * H2S_LOW
        H2S_high_kg_s = hot_outflow * H2S_HIGH


        # convert to tonnes/year
        H2S_low_t_yr = (
            H2S_low_kg_s
            * SECONDS_PER_YEAR
            / 1000.0
        )

        H2S_high_t_yr = (
            H2S_high_kg_s
            * SECONDS_PER_YEAR
            / 1000.0
        )


        # ----------------------------------------------------
        # DEPOSITION RATES
        #
        # Apply same efficiency scenarios used by Andersen
        # ----------------------------------------------------

        H2S_low_dep_2_5 = H2S_low_t_yr * EFF_LOW
        H2S_low_dep_5 = H2S_low_t_yr * EFF_MID
        H2S_low_dep_10 = H2S_low_t_yr * EFF_HIGH

        H2S_high_dep_2_5 = H2S_high_t_yr * EFF_LOW
        H2S_high_dep_5 = H2S_high_t_yr * EFF_MID
        H2S_high_dep_10 = H2S_high_t_yr * EFF_HIGH


        time_years = time_seconds / SECONDS_PER_YEAR


        results.append({

            "Time_s": time_seconds,
            "Time_years": time_years,

            "Total_outflow_kg_s": total_outflow,
            "Recharge_kg_s": recharge,
            "NetFlux_kg_s": net_flux,

            "Hot_outflow_kg_s": hot_outflow,
            "Hot_fraction": hot_fraction,

            "H2S_low_27ppm_kg_s": H2S_low_kg_s,
            "H2S_high_85ppm_kg_s": H2S_high_kg_s,

            "H2S_low_27ppm_t_yr": H2S_low_t_yr,
            "H2S_high_85ppm_t_yr": H2S_high_t_yr,

            "H2S_low_dep_2.5pct_t_yr": H2S_low_dep_2_5,
            "H2S_low_dep_5pct_t_yr": H2S_low_dep_5,
            "H2S_low_dep_10pct_t_yr": H2S_low_dep_10,

            "H2S_high_dep_2.5pct_t_yr": H2S_high_dep_2_5,
            "H2S_high_dep_5pct_t_yr": H2S_high_dep_5,
            "H2S_high_dep_10pct_t_yr": H2S_high_dep_10,

            "Number_outflow_faces": outflow_faces,
            "Number_hot_faces": hot_faces
        })


        print(
            f"{time_years:9.2f} yr   "
            f"hot={hot_outflow:10.4e} kg/s   "
            f"H2S(27ppm)={H2S_low_t_yr:10.4e} t/yr   "
            f"H2S(85ppm)={H2S_high_t_yr:10.4e} t/yr"
        )


    except Exception as e:

        print(f"ERROR at time {dirname}: {e}")


# ------------------------------------------------------------
# CUMULATIVE H2S DEPOSITION
#
# Trapezoidal integration
# ------------------------------------------------------------

cum_low_2_5 = 0.0
cum_low_5 = 0.0
cum_low_10 = 0.0

cum_high_2_5 = 0.0
cum_high_5 = 0.0
cum_high_10 = 0.0


for i in range(len(results)):

    if i == 0:

        results[i]["Cum_H2S_low_2.5pct_t"] = 0.0
        results[i]["Cum_H2S_low_5pct_t"] = 0.0
        results[i]["Cum_H2S_low_10pct_t"] = 0.0

        results[i]["Cum_H2S_high_2.5pct_t"] = 0.0
        results[i]["Cum_H2S_high_5pct_t"] = 0.0
        results[i]["Cum_H2S_high_10pct_t"] = 0.0

        continue


    dt_years = (
        results[i]["Time_years"]
        - results[i-1]["Time_years"]
    )


    # --------------------------------------------------------
    # LOW H2S = 27 ppm
    # --------------------------------------------------------

    cum_low_2_5 += 0.5 * (
        results[i-1]["H2S_low_dep_2.5pct_t_yr"]
        +
        results[i]["H2S_low_dep_2.5pct_t_yr"]
    ) * dt_years

    cum_low_5 += 0.5 * (
        results[i-1]["H2S_low_dep_5pct_t_yr"]
        +
        results[i]["H2S_low_dep_5pct_t_yr"]
    ) * dt_years

    cum_low_10 += 0.5 * (
        results[i-1]["H2S_low_dep_10pct_t_yr"]
        +
        results[i]["H2S_low_dep_10pct_t_yr"]
    ) * dt_years


    # --------------------------------------------------------
    # HIGH H2S = 85 ppm
    # --------------------------------------------------------

    cum_high_2_5 += 0.5 * (
        results[i-1]["H2S_high_dep_2.5pct_t_yr"]
        +
        results[i]["H2S_high_dep_2.5pct_t_yr"]
    ) * dt_years

    cum_high_5 += 0.5 * (
        results[i-1]["H2S_high_dep_5pct_t_yr"]
        +
        results[i]["H2S_high_dep_5pct_t_yr"]
    ) * dt_years

    cum_high_10 += 0.5 * (
        results[i-1]["H2S_high_dep_10pct_t_yr"]
        +
        results[i]["H2S_high_dep_10pct_t_yr"]
    ) * dt_years


    results[i]["Cum_H2S_low_2.5pct_t"] = cum_low_2_5
    results[i]["Cum_H2S_low_5pct_t"] = cum_low_5
    results[i]["Cum_H2S_low_10pct_t"] = cum_low_10

    results[i]["Cum_H2S_high_2.5pct_t"] = cum_high_2_5
    results[i]["Cum_H2S_high_5pct_t"] = cum_high_5
    results[i]["Cum_H2S_high_10pct_t"] = cum_high_10


# ------------------------------------------------------------
# WRITE CSV
# ------------------------------------------------------------

fieldnames = [

    "Time_s",
    "Time_years",

    "Total_outflow_kg_s",
    "Recharge_kg_s",
    "NetFlux_kg_s",

    "Hot_outflow_kg_s",
    "Hot_fraction",

    "H2S_low_27ppm_kg_s",
    "H2S_high_85ppm_kg_s",

    "H2S_low_27ppm_t_yr",
    "H2S_high_85ppm_t_yr",

    "H2S_low_dep_2.5pct_t_yr",
    "H2S_low_dep_5pct_t_yr",
    "H2S_low_dep_10pct_t_yr",

    "H2S_high_dep_2.5pct_t_yr",
    "H2S_high_dep_5pct_t_yr",
    "H2S_high_dep_10pct_t_yr",

    "Cum_H2S_low_2.5pct_t",
    "Cum_H2S_low_5pct_t",
    "Cum_H2S_low_10pct_t",

    "Cum_H2S_high_2.5pct_t",
    "Cum_H2S_high_5pct_t",
    "Cum_H2S_high_10pct_t",

    "Number_outflow_faces",
    "Number_hot_faces"
]


with open(output_file, "w", newline="") as f:

    writer = csv.DictWriter(
        f,
        fieldnames=fieldnames
    )

    writer.writeheader()

    for row in results:
        writer.writerow(row)

# ------------------------------------------------------------
# PLOT CUMULATIVE H2S / SULPHIDE ACCUMULATION
# ------------------------------------------------------------

if results:

    time_years = [
        r["Time_years"]
        for r in results
    ]

    # 27 ppm cases
    cum_low_2_5 = [
        r["Cum_H2S_low_2.5pct_t"]
        for r in results
    ]

    cum_low_5 = [
        r["Cum_H2S_low_5pct_t"]
        for r in results
    ]

    cum_low_10 = [
        r["Cum_H2S_low_10pct_t"]
        for r in results
    ]

    # 85 ppm cases
    cum_high_2_5 = [
        r["Cum_H2S_high_2.5pct_t"]
        for r in results
    ]

    cum_high_5 = [
        r["Cum_H2S_high_5pct_t"]
        for r in results
    ]

    cum_high_10 = [
        r["Cum_H2S_high_10pct_t"]
        for r in results
    ]


    plt.figure(figsize=(9, 6))

    # 27 ppm
    plt.plot(
        time_years,
        cum_low_2_5,
        label="27 ppm, 2.5% efficiency",
        linewidth=2
    )

    plt.plot(
        time_years,
        cum_low_5,
        label="27 ppm, 5% efficiency",
        linewidth=2
    )

    plt.plot(
        time_years,
        cum_low_10,
        label="27 ppm, 10% efficiency",
        linewidth=2
    )

    # 85 ppm
    plt.plot(
        time_years,
        cum_high_2_5,
        label="85 ppm, 2.5% efficiency",
        linewidth=2,
        linestyle="--"
    )

    plt.plot(
        time_years,
        cum_high_5,
        label="85 ppm, 5% efficiency",
        linewidth=2,
        linestyle="--"
    )

    plt.plot(
        time_years,
        cum_high_10,
        label="85 ppm, 10% efficiency",
        linewidth=2,
        linestyle="--"
    )


    plt.xlabel("Time (years)")
    plt.ylabel("Cumulative H$_2$S deposition (tonnes)")

    plt.title(
        "Cumulative H$_2$S deposition from >350 °C hydrothermal discharge"
    )

    plt.grid(True, alpha=0.3)

    plt.legend(
        frameon=False,
        fontsize=9
    )

    plt.tight_layout()

    plot_file = "andersen_H2S_accumulation.png"

    plt.savefig(
        plot_file,
        dpi=300,
        bbox_inches="tight"
    )

    print(f"Saved plot: {plot_file}")

    plt.show()
# ------------------------------------------------------------
# FINAL SUMMARY
# ------------------------------------------------------------

print()
print("-" * 120)
print(f"Saved: {output_file}")


if results:

    max_hot = max(
        r["Hot_outflow_kg_s"]
        for r in results
    )

    final = results[-1]

    print()
    print(f"Maximum >350 C discharge : {max_hot:.6e} kg/s")

    print()
    print("Cumulative H2S deposition:")

    print(
        f"27 ppm, 2.5% : "
        f"{final['Cum_H2S_low_2.5pct_t']:.3f} t"
    )

    print(
        f"27 ppm, 5%   : "
        f"{final['Cum_H2S_low_5pct_t']:.3f} t"
    )

    print(
        f"27 ppm, 10%  : "
        f"{final['Cum_H2S_low_10pct_t']:.3f} t"
    )

    print()

    print(
        f"85 ppm, 2.5% : "
        f"{final['Cum_H2S_high_2.5pct_t']:.3f} t"
    )

    print(
        f"85 ppm, 5%   : "
        f"{final['Cum_H2S_high_5pct_t']:.3f} t"
    )

    print(
        f"85 ppm, 10%  : "
        f"{final['Cum_H2S_high_10pct_t']:.3f} t"
    )

print()
