from datetime import datetime,timezone
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, ForeignKey, UniqueConstraint, Enum
from database import Base
from shemas.roles import TenantRole

class TenantMembershipDB(Base):

    __tablename__ = "TenantMemberships"
    __table_args__ = (
        UniqueConstraint("tenant_id","user_id",name="uq_membership_tenant_user"),
        )

    id : Mapped[int] = mapped_column(primary_key=True ,autoincrement=True)
    tenant_id : Mapped[int] = mapped_column(ForeignKey("Tenants.id", ondelete="CASCADE"))
    user_id : Mapped[int] = mapped_column(ForeignKey("Users.id", ondelete="CASCADE"), index=True)
    tenant_role : Mapped[TenantRole] =  mapped_column(Enum(TenantRole))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default = lambda: datetime.now(timezone.utc))