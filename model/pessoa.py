from sqlalchemy import Column, String, Integer, ForeignKey
from model.base import Base

class Pessoa(Base):
    __tablename__ = 'pessoa'

    id = Column("pk_pessoa", Integer, primary_key=True)
    nome = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False)

    # Definição do relacionamento entre a pessoa e o evento.
    evento_id = Column(Integer, ForeignKey("evento.pk_evento"), nullable=False)

    def __init__(self, nome: str, email: str, evento_id: int):
        """
        Cria uma Pessoa

        Arguments:
            nome: nome da pessoa.
            email: email da pessoa.
            evento_id: id do evento ao qual a pessoa se inscreveu.
        """
        self.nome = nome
        self.email = email
        self.evento_id = evento_id
