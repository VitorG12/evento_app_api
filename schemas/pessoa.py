from pydantic import BaseModel

class PessoaSchema(BaseModel):
    """ Define como uma nova pessoa a ser inserida deve ser representada
    """
    nome: str = "Vitor Gabriel"
    email: str = "vitor@email.com"
    evento_id: int = 1

class PessoaViewSchema(BaseModel):
    """ Define como uma pessoa será retornada
    """
    id: int = 1
    nome: str = "Vitor Gabriel"
    email: str = "vitor@email.com"
    evento_id: int = 1
