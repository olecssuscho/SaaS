from datetime import datetime,timezone
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime
from database import Base

class UserDB(Base):

    __tablename__ = "Users"

    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email : Mapped[str]
    password : Mapped[str]
    fullname : Mapped[str]
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), default = lambda: datetime.now(timezone.utc))