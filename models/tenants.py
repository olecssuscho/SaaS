from datetime import datetime,timezone
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, ForeignKey, String
from database import Base

class TenantDB(Base):

    __tablename__ = "Tenants"

    id : Mapped[int] = mapped_column(primary_key=True ,autoincrement=True)
    name  : Mapped[str] = mapped_column(String(50),unique=True)
    plane_id : Mapped[int] = mapped_column(ForeignKey("Plans.id", ondelete="RESTRICT"))
    subscription_status : Mapped[int] = mapped_column(ForeignKey("Statuses.id", ondelete="RESTRICT"))
    current_period_end : Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default = lambda: datetime.now(timezone.utc))