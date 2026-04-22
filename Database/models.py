from sqlmodel import SQLModel, Field
from typing import Optional


class SalesTransaction(SQLModel, table=True):
    __tablename__ = "salestransaction"
    __table_args__ = {"extend_existing": True}

    id: Optional[int] = Field(default=None, primary_key=True)

    order_date: str
    product_name: str
    category: str
    region: str
    customer_segment: str

    quantity: int
    unit_price: float
    unit_variable_cost: float

    revenue: float
    variable_cost: float
    contribution_margin: float
    margin_ratio: float

    year: int
    month: int
    quarter: str
