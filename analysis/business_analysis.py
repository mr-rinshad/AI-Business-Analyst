from analysis.analysis_engine import (
    load_orders,
    analyze_monthly_revenue,
    analyze_monthly_category_revenue
)

def analyze_revenue_drop():

    orders = load_orders()

    monthly_revenue = analyze_monthly_revenue(
        orders
    )

    return monthly_revenue

def find_largest_revenue_drop(monthly_revenue):

    valid_changes = monthly_revenue.dropna(
        subset=["revenue_change"]
    )

    if valid_changes.empty:
        return None

    largest_drop = valid_changes.loc[
        valid_changes["revenue_change"].idxmin()
    ]

    return largest_drop


def get_category_changes(
    orders,
    previous_month,
    current_month
):

    monthly_category = (
        analyze_monthly_category_revenue(
            orders
        )
    )

    previous = monthly_category[
        monthly_category["month"] == previous_month
    ]

    current = monthly_category[
        monthly_category["month"] == current_month
    ]

    comparison = previous.merge(
        current,
        on="category",
        how="outer",
        suffixes=("_previous", "_current")
    )

    comparison[
        "revenue_change"
    ] = (
        comparison["revenue_current"].fillna(0)
        -
        comparison["revenue_previous"].fillna(0)
    )

    return comparison.sort_values(
        "revenue_change"
    )


if __name__ == "__main__":

    orders = load_orders()

    monthly_revenue = analyze_monthly_revenue(
        orders
    )

    largest_drop = find_largest_revenue_drop(
        monthly_revenue
    )

    print("\nLargest Revenue Drop:")
    print(largest_drop)

    current_month = int(
        largest_drop["month"]
    )

    previous_month = current_month - 1

    category_changes = get_category_changes(
        orders,
        previous_month,
        current_month
    )

    print("\nCategory Changes:")
    print(category_changes)