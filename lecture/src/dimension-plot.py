import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def main():
    data = pd.DataFrame.from_records(
        [
            ("Bulbasaur", 45, 49, 49, 65, 65, 45, "#43B02A"),
            ("Charmander", 39, 52, 43, 60, 50, 65, "#C8102E"),
            ("Squirtle", 44, 48, 65, 50, 64, 43, "#00A3E0"),
            ("Pikachu", 35, 55, 30, 50, 40, 90, "#FFB81C"),
        ],
        columns=[
            "Pokemon",
            "HP",
            "Attack",
            "Defense",
            "Special Attack",
            "Special Defence",
            "Speed",
            "Color",
        ],
    )

    sns.set_style("whitegrid")
    sns.set_context("poster")
    plt.figure(figsize=(12, 12))
    plt.subplot(polar=True)

    stats = data.columns.values[1:-1]
    theta = np.linspace(0, 2 * np.pi, len(stats), endpoint=False)
    lines, labels = plt.thetagrids(range(0, 360, int(360 / len(stats))), (stats))

    for index, row in data.iterrows():
        print(row["Pokemon"], row["Color"])
        cstats = row[stats].tolist()
        cstats = np.concatenate((cstats, [cstats[0]]))
        print(cstats)
        angles = np.concatenate((theta, [theta[0]]))
        plt.plot(angles, cstats, label=row["Pokemon"], color=row["Color"])
        plt.fill(angles, cstats, row["Color"], alpha=0.1)

    plt.legend(
        loc="upper center",
        ncol=2,
        frameon=False,
        bbox_to_anchor=(0.5, -0.05),
    )
    plt.title("Initial Characteristics of Starter Pokemon (1st Gen)")
    plt.savefig(os.path.join("img", "dimension-plot.pdf"))


if __name__ == "__main__":
    main()
