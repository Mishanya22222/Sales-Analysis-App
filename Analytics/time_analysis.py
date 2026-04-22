from sqlmodel import select, func
from Database.db import get_session
from Database.models import SalesTransaction

def revenue_over_time():
    with get_session() as session:

        results = session.exec(
            select(
                SalesTransaction.order_date,
                func.sum(SalesTransaction.revenue)
            )
            .group_by(SalesTransaction.order_date)
        ).all()

    return results