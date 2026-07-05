from pydantic import BaseModel
from typing import Optional, List
from model.evento import Evento

from schemas.pessoa import PessoaViewSchema

class EventoSchema(BaseModel):
    """ Define como um novo evento a ser inserido deve ser representado
    """
    nome: str = "Universo TOTVS 2026"
    descricao: Optional[str] = "O maior evento de tecnologia e negócios do Brasil"
    data_hora: str = "13/10/2026 14:00"
    local: str = "Expo Center Norte - São Paulo - SP"
    categoria: str = "Conferência"

class EventoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca por id.
    """
    id: int = 1

class EventoBuscaCategoriaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca por categoria.
    """
    categoria: str = "Conferência"

class EventoViewSchema(BaseModel):
    """ Define como um evento será retornado: evento + inscritos.
    """
    id: int = 1
    nome: str = "Universo TOTVS 2026"
    descricao: Optional[str] = "O maior evento de tecnologia e negócios do Brasil"
    data_hora: str = "13/10/2026 14:00"
    local: str = "Expo Center Norte - São Paulo - SP"
    categoria: str = "Conferência"
    total_inscritos: int = 1
    inscritos: List[PessoaViewSchema]

class ListagemEventosSchema(BaseModel):
    """ Define como uma listagem de eventos será retornada.
    """
    eventos: List[EventoViewSchema]

class EventoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    message: str
    id: int

def apresenta_evento(evento: Evento):
    """ Retorna uma representação do evento seguindo o schema definido em
        EventoViewSchema.
    """
    return {
        "id": evento.id,
        "nome": evento.nome,
        "descricao": evento.descricao,
        "data_hora": evento.data_hora,
        "local": evento.local,
        "categoria": evento.categoria,
        "total_inscritos": len(evento.inscritos),
        "inscritos": [{"id": i.id, "nome": i.nome, "email": i.email, "evento_id": i.evento_id} for i in evento.inscritos]
    }

def apresenta_eventos(eventos: List[Evento]):
    """ Retorna uma representação dos eventos seguindo o schema definido em
        ListagemEventosSchema.
    """
    result = []
    for evento in eventos:
        result.append({
            "id": evento.id,
            "nome": evento.nome,
            "descricao": evento.descricao,
            "data_hora": evento.data_hora,
            "local": evento.local,
            "categoria": evento.categoria,
            "total_inscritos": len(evento.inscritos),
            "inscritos": [{"id": i.id, "nome": i.nome, "email": i.email, "evento_id": i.evento_id} for i in evento.inscritos]
        })

    return {"eventos": result}
