import os
import matplotlib.pyplot as plt
import pandas as pd


CHART_DIR = "outputs/charts"


def create_chart(
    data,
    chart_type,
    x_column,
    y_column,
    title,
    filename
):

    os.makedirs(CHART_DIR, exist_ok=True)

    plt.figure(figsize=(10, 6))

    if chart_type == "line":

        plt.plot(
            data[x_column],
            data[y_column],
            marker="o"
        )

    elif chart_type == "bar":

        plt.bar(
            data[x_column],
            data[y_column]
        )

    elif chart_type == "scatter":

        plt.scatter(
            data[x_column],
            data[y_column]
        )

    else:

        raise ValueError(
            f"Unsupported chart type: {chart_type}"
        )

    plt.title(title)
    plt.xlabel(x_column)
    plt.ylabel(y_column)

    plt.xticks(rotation=45)

    plt.tight_layout()

    filepath = os.path.join(
        CHART_DIR,
        filename
    )

    plt.savefig(filepath)

    plt.close()

    return filepath

if __name__ == "__main__":

    data = pd.DataFrame({
        "month": ["January", "February", "March"],
        "revenue": [159450, 122700, 127200]
    })

    filepath = create_chart(
        data=data,
        chart_type="line",
        x_column="month",
        y_column="revenue",
        title="Monthly Revenue",
        filename="test_revenue.png"
    )

    print("Chart created:")
    print(filepath)