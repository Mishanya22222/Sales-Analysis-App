from sqlmodel import select, func
from Database.db import get_session
from Database.models import SalesTransaction

def growth_rate_over_time(selected_category: str = "All", selected_region: str = "All"):
    with get_session() as session:
        query = (
            select(
                SalesTransaction.quarter,
                func.sum(SalesTransaction.revenue),
            )
            .group_by(SalesTransaction.quarter)
            .order_by(SalesTransaction.quarter)
        )

        if selected_category != "All":
            query = query.where(SalesTransaction.category == selected_category)

        if selected_region != "All":
            query = query.where(SalesTransaction.region == selected_region)

        results = session.exec(query).all()

    growth_rates = []
    previous_revenue = None

    for quarter, revenue in results:
        if previous_revenue is not None and previous_revenue > 0:
            growth_rate = (revenue - previous_revenue) / previous_revenue
        else:
            growth_rate = 0.0

        growth_rates.append((quarter, growth_rate))
        previous_revenue = revenue

    return growth_rates