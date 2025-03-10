from core.database import Base
from sqlalchemy.orm import Mapped, mapped_column


class PasswordModel(Base):
    __tablename__ = 'passwords'

    id: Mapped[int] = mapped_column(primary_key=True)
    service_name: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
