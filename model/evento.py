from sqlalchemy import Column, String, Integer, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from model.base import Base

class Evento(Base):
    __tablename__ = 'evento'

    id = Column("pk_evento", Integer, primary_key=True)
    nome = Column(String(200), unique=True, nullable=False)
    descricao = Column(Text, nullable=True)
    data_hora = Column(String(50), nullable=False)
    local = Column(String(200), nullable=False)
    categoria = Column(String(100), nullable=False)
    data_insercao = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre o evento e as pessoas (inscritos).
    inscritos = relationship("Pessoa")

    def __init__(self, nome: str, data_hora: str, local: str, categoria: str, 
                 descricao: str = None, data_insercao: DateTime = None):
        """
        Cria um Evento

        Arguments:
            nome: nome do evento.
            data_hora: data e hora do evento.
            local: local do evento.
            categoria: categoria do evento.
            descricao: descricao do evento.
            data_insercao: data de quando o evento foi inserido à base.
        """
        self.nome = nome
        self.descricao = descricao
        self.data_hora = data_hora
        self.local = local
        self.categoria = categoria

        if data_insercao:
            self.data_insercao = data_insercao

    def adiciona_pessoa(self, pessoa: 'Pessoa'):
        self.inscritos.append(pessoa)
