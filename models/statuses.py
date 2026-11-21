from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text
from database import Base

class StatusDB(Base):

    __tablename__ = "Statuses"

    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(String(50),unique=True)
    description : Mapped[str] = mapped_column(Text)

    