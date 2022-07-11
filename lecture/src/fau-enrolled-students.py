import os

import matplotlib.pyplot as plt
import pandas as pd
from pywaffle import Waffle


def main():
    data = pd.DataFrame.from_records(
        [
            (
                "Faculty of Humanities, Social Sciences, and Theology",
                9476,
                "#FFB81C",
                "#E87722",
            ),
            ("Faculty of Business, Economics, and Law", 9962, "#C8102E", "#971B2F"),
            ("Faculty of Medicine", 4106, "#00A3E0", "#0061A0"),
            ("Faculty of Sciences", 5326, "#43B02A", "#228848"),
            ("Faculty of Engineering", 10008, "#779FB5", "#41748D"),
        ],
        columns=["Faculty", "Students", "Color", "Color Dark"],
    )

    plt.figure(
        FigureClass=Waffle,
        rows=5,
        values=[int(n / 500) for n in data["Students"].tolist()],
        colors=data["Color"].tolist(),
        icons="person",
        block_arranging_style="snake",
        interval_ratio_x=0.1,
        interval_ratio_y=0.2,
        font_size=29,
        icon_legend=False,
        legend={
            "labels": [
                f"{f} ({n:,})"
                for f, n in zip(data["Faculty"].tolist(), data["Students"].tolist())
            ],
            "loc": "upper center",  # 'upper left',
            "ncol": 2,
            "bbox_to_anchor": (0.5, -0.05),  # (1, 1)
        },
        vertical=True,
        figsize=(8, 5),
    )
    plt.title("Number of Students in Winter Semester 2020/21")
    plt.tight_layout()
    plt.savefig(os.path.join("img", "fau-enrolled-students.pdf"))


if __name__ == "__main__":
    main()
