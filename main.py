import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
import matplotlib.colors as mcolors

from macroregions import macroregions

COLORMAP = 'gist_rainbow'

df = pd.read_csv("data/input_data.csv")
df["Region"] = df["Область"].astype(str).str.strip()
df["City/District"] = df["Місто/Район"].astype(str).str.strip()
df["Value"] = pd.to_numeric(df["Значення"], errors="coerce")
df = df.groupby(["Region", "City/District"], as_index=False)["Value"].mean()
duplicates = df.duplicated(subset=["Region", "City/District"])

def draw_bar_chart(chart_name, names, values, title, xlabel="Value", show_mean=True):
    """
    Draws a horizontal bar chart with colormap and colorbar.
    
    Parameters:
    - chart_name: filename for saving the figure
    - names: list of labels (cities/districts or regions)
    - values: corresponding numerical values
    - title: chart title
    - xlabel: label for X-axis
    - show_mean: whether to show mean line
    """

    norm = mcolors.Normalize(vmin=min(values), vmax=max(values))
    cmap = cm.get_cmap(COLORMAP)
    colors = [cmap(norm(v)) for v in values]
    mean_val = np.mean(values)

    fig, ax = plt.subplots(figsize=(16, 9))
    bars = ax.barh(names, values, color=colors)
    
    if show_mean:
        ax.axvline(mean_val, color="black", linestyle="--", linewidth=2, label=f"Mean: {mean_val:.1f}")

    for bar in bars:
        width = bar.get_width()
        ax.text(width + (max(values) - min(values)) * 0.01,
                bar.get_y() + bar.get_height() / 2,
                f"{width:.1f}",
                va="center", fontsize=9)

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, orientation="vertical", pad=0.02)
    cbar.set_label(xlabel, fontsize=11)

    ax.set_title(title, fontsize=14)
    ax.set_xlabel(xlabel)
    ax.grid(True, axis="x", linestyle="--", alpha=0.4)
    plt.tight_layout(pad=0.3)
    plt.legend()
    plt.margins(0)
    plt.xlim(min(values) * 0.98, max(values) * 1.02)
    plt.subplots_adjust(top=0.94, bottom=0.06)
    plt.savefig(f"results/{chart_name}.png")
    plt.show()


def plot_region_chart(df):
    "Displays statistics by selected region."

    regions = sorted(df["Region"].unique())
    print("\nSelect a region:")
    for i, reg in enumerate(regions, 1):
        print(f"{i}. {reg}")

    try:
        n = int(input("\nEnter region number: "))
        region = regions[n - 1]
    except (ValueError, IndexError):
        print("Invalid selection!")
        return

    subset = df[df["Region"] == region].copy()
    subset = subset.sort_values("Value", ascending=True).reset_index(drop=True)
    
    draw_bar_chart('region_chart', subset["City/District"].tolist(), subset["Value"].tolist(),
                   title=f"Value distribution by districts: {region}")


def plot_macroregion_chart(df):
    """
    Displays average statistics by selected macroregion.
    """
    print("\nSelect a macroregion:")
    for i, reg in enumerate(macroregions.keys(), 1):
        print(f"{i}. {reg}")

    try:
        n = int(input("\nEnter macroregion number: "))
        macro_name = list(macroregions.keys())[n - 1]
    except (ValueError, IndexError):
        print("Invalid selection!")
        return

    selected_regions = macroregions[macro_name]
    subset = df[df["Region"].isin(selected_regions)]
    
    region_mean = subset.groupby("Region")["Value"].mean().sort_values()
    
    draw_bar_chart('macroregion_chart', region_mean.index.tolist(), region_mean.values.tolist(),
                   title=f"Average values by regions in macroregion: {macro_name}",
                   xlabel="Average Value")


def plot_all_regions_comparison(df):
    """
    Displays average statistics across all regions.
    """
    comp_df = df.groupby("Region")["Value"].mean().sort_values()
    draw_bar_chart('country_chart', comp_df.index.tolist(), comp_df.values.tolist(),
                   title="Comparison of average values across all regions",
                   xlabel="Average Value")



def start_app():
    """
    Starts the interactive menu-driven application.
    """
    while True:
        print("\nSelect chart type:")
        print("1. By region")
        print("2. By macroregion")
        print("3. Compare all regions")
        print("0. Exit")

        choice = input("\nYour choice: ")
        if choice == "1":
            plot_region_chart(df)
        elif choice == "2":
            plot_macroregion_chart(df)
        elif choice == "3":
            plot_all_regions_comparison(df)
        elif choice == "0":
            print("Exiting the application.")
            break
        else:
            print("Invalid command, please try again.")


if __name__ == "__main__":
    start_app()