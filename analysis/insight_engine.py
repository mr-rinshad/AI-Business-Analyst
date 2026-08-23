from analysis.analysis_engine import (
    load_orders,
    calculate_total_revenue,
    calculate_total_profit,
    calculate_total_orders,
    calculate_average_order_value,
    analyze_monthly_revenue,
    analyze_category_revenue,
    analyze_customer_revenue,
    analyze_monthly_category_revenue
)

def detect_revenue_change(monthly_revenue):

    month_names = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December"
    }

    insights = []

    for _, row in monthly_revenue.iterrows():

        change = row["revenue_change"]

        if change != change:
            continue

        month = int(row["month"])
        month_name = month_names[month]

        if change < 0:

            insights.append(
                f"Revenue decreased by {abs(change):.2f}% "
                f"in {month_name}."
            )

        elif change > 0:

            insights.append(
                f"Revenue increased by {change:.2f}% "
                f"in {month_name}."
            )

    return insights

def detect_top_category(category_revenue):

    if category_revenue.empty:
        return None

    top_category = category_revenue.iloc[0]

    return (
        f"{top_category['category']} generated the highest revenue "
        f"of {top_category['revenue']:.2f}."
    )


def detect_top_customer(customer_revenue):

    if customer_revenue.empty:
        return None

    top_customer = customer_revenue.iloc[0]

    return (
        f"{top_customer['customer_name']} generated the highest "
        f"customer revenue of {top_customer['revenue']:.2f}."
    )




if __name__ == "__main__":

    orders = load_orders()

    monthly_revenue = analyze_monthly_revenue(orders)
    category_revenue = analyze_category_revenue(orders)
    customer_revenue = analyze_customer_revenue(orders)
    monthly_category = analyze_monthly_category_revenue(orders)

    top_customer_insight = detect_top_customer(customer_revenue)

    revenue_insights = detect_revenue_change(monthly_revenue)

    top_category_insight = detect_top_category(category_revenue)

    monthly_category = analyze_monthly_category_revenue(orders)

    print("\nMonthly Category Revenue:")
    print(monthly_category)

    print("\nBusiness Insights:")

    for insight in revenue_insights:
        print("-", insight)

    print("-", top_category_insight)

    print("-", top_customer_insight)

    print("\nMonthly Category Revenue:")
    print(monthly_category)