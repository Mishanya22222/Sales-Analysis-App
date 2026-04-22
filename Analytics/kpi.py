from sqlmodel import select, func, desc
from Database.db import get_session
from Database.models import SalesTransaction


def get_kpis():
    with get_session() as session:

        revenue = session.exec(
            select(SalesTransaction.revenue)
        ).all()

        margin = session.exec(
            select(SalesTransaction.contribution_margin)
        ).all()

        total_revenue = sum(revenue)
        total_margin = sum(margin)

        ratio = total_margin / total_revenue if total_revenue else 0

    return {
        "revenue": total_revenue,
        "margin": total_margin,
        "margin_ratio": ratio
    }

def top_products(limit=5):
    with get_session() as session:

        results = session.exec(
            select(
                SalesTransaction.product_name,
                func.sum(SalesTransaction.revenue)
            )
            .group_by(SalesTransaction.product_name)
            .order_by(desc(func.sum(SalesTransaction.revenue)))
            .limit(limit)
        ).all()

    return results