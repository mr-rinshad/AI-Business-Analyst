import time

from analysis.chart_selector import select_chart
from analysis.chart_engine import create_chart


def visualize_result(
    question,
    data
):

    if data is None or data.empty:
        return None

    chart_config = select_chart(
        question,
        data
    )

    if chart_config is None:
        return None

    filename = (
        f"chart_{int(time.time())}.png"
    )

    filepath = create_chart(
        data=data,
        chart_type=chart_config["chart_type"],
        x_column=chart_config["x_column"],
        y_column=chart_config["y_column"],
        title=chart_config["title"],
        filename=filename
    )

    return filepath