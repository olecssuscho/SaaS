from datetime import datetime,timezone
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, String
from database import Base

class PlaneDB(Base):

    __tablename__ = "Plans"

    id : Mapped[int] = mapped_column(primary_key=True)
    name  : Mapped[str] = mapped_column(String(50),unique=True)
    price_cents: Mapped[int]
    max_links: Mapped[int]
    max_clicks_per_month: Mapped[int]
    max_members: Mapped[int]
    analytics_retention_days: Mapped[int]
    allow_custom_domain: Mapped[bool] = mapped_column(default=False)
    allow_api: Mapped[bool] = mapped_column(default=False)
    is_active : Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default = lambda: datetime.now(timezone.utc))