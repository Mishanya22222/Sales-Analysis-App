from sqlmodel import select, func
from Database.db import get_session
from Database.models import SalesTransaction

def revenue_over_time(selected_category: str = "All", selected_region: str = "All"):
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

    return results
