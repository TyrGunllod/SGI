from sqlalchemy import Column, String, Boolean, text
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
import uuid

class AppModel(Base):
    __tablename__ = "modules_apps"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)           # Ex: "Financeiro"
    description = Column(String, nullable=True)     # Ex: "Gestão de Contas"
    icon = Column(String, default="Package")        # Nome do ícone no Lucide
    path = Column(String, unique=True, nullable=False) # Ex: "/finance"
    is_active = Column(Boolean, default=True)