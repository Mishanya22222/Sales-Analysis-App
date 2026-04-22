from sqlmodel import select, func
from Database.db import get_session
from Database.models import SalesTransaction

def avg_order_value(selected_category: str = "All", selected_region: str = "All"):
    with get_session() as session:
        query = (
            select(
                SalesTransaction.quarter,
                func.sum(SalesTransaction.revenue),
                func.sum(SalesTransaction.quantity)
            )
            .group_by(SalesTransaction.quarter)
            .order_by(SalesTransaction.quarter)
        )

        if selected_category != "All":
            query = query.where(SalesTransaction.category == selected_category)

        if selected_region != "All":
            query = query.where(SalesTransaction.region == selected_region)

        results = session.exec(query).all()

    avg_values = []
    for quarter, total_revenue, total_quantity in results:
        avg_value = total_revenue / total_quantity if total_quantity else 0
        avg_values.append((quarter, avg_value))

    return avg_values