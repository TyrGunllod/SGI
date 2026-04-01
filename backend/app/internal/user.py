from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text
from app.database.base import Base

class User(Base):

    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String, unique=True, nullable=False)

    senha_hash = Column(String, nullable=False)

    nome = Column(String)

    ativo = Column(Boolean, default=True)

    criado_em = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))