from analysis.business_analysis import compare_months, get_connection
from analysis.category_analysis import analyze_categories
from analysis.product_analysis import analyze_products
from analysis.customer_analysis import analyze_customers
from analysis.region_analysis import analyze_regions
from analysis.segment_analysis import analyze_segments
from analysis.month_extractor import get_investigation_months


# --------------------------------
# Main Investigation Engine
# --------------------------------
def investigate_business_change(
    question,
    metric="revenue"
):
    previous_month, current_month = (
        get_investigation_months(question)
    )

    # --------------------------------
    # Overall Comparison
    # --------------------------------
    connection = get_connection()
    try:
        comparison = compare_months(
            connection,
            previous_month,
            current_month
        )
    finally:
        connection.close()

    # --------------------------------
    # Category Analysis
    # --------------------------------
    categories = analyze_categories(
        previous_month,
        current_month,
        metric
    )

    # --------------------------------
    # Product Analysis
    # --------------------------------
    products = analyze_products(
        previous_month,
        current_month,
        metric
    )

    # --------------------------------
    # Customer Analysis
    # --------------------------------
    customers = analyze_customers(
        previous_month,
        current_month,
        metric
    )

    # --------------------------------
    # Region Analysis
    # --------------------------------
    regions = analyze_regions(
        previous_month,
        current_month,
        metric
    )

    # --------------------------------
    # Segment Analysis
    # --------------------------------
    segments = analyze_segments(
        previous_month,
        current_month,
        metric
    )

    # --------------------------------
    # Combined Investigation
    # --------------------------------
    return {
        "metric": metric,
        "previous_month": previous_month,
        "current_month": current_month,
        "comparison": comparison,
        "categories": categories,
        "products": products,
        "customers": customers,
        "regions": regions,
        "segments": segments
    }


# --------------------------------
# Test
# --------------------------------
if __name__ == "__main__":
    test_question = "Why did revenue drop in March compared to February?"

    result = investigate_business_change(
        question=test_question,
        metric="revenue"
    )

    print("\nCombined Business Investigation:")
    print(result)