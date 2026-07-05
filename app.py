from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect

from sqlalchemy.exc import IntegrityError

from model import Session, Evento, Pessoa
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Evento App API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
evento_tag = Tag(name="Evento", description="Adição, visualização, remoção e filtragem de eventos")
pessoa_tag = Tag(name="Pessoa", description="Inscrição de pessoas em eventos")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/evento', tags=[evento_tag],
          responses={"200": EventoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_evento(form: EventoSchema):
    """Adiciona um novo Evento à base de dados

    Retorna uma representação dos eventos e pessoas associadas.
    """
    evento = Evento(
        nome=form.nome,
        descricao=form.descricao,
        data_hora=form.data_hora,
        local=form.local,
        categoria=form.categoria
    )
    logger.debug(f"Adicionando evento de nome: '{evento.nome}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando evento
        session.add(evento)
        # efetivando o comando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado evento de nome: '{evento.nome}'")
        return apresenta_evento(evento), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Evento de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar evento '{evento.nome}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo evento :/"
        logger.warning(f"Erro ao adicionar evento '{evento.nome}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/eventos', tags=[evento_tag],
         responses={"200": ListagemEventosSchema})
def get_eventos():
    """Faz a busca por todos os Eventos cadastrados

    Retorna uma representação da listagem de eventos.
    """
    logger.debug(f"Coletando eventos")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    eventos = session.query(Evento).all()

    if not eventos:
        # se não há eventos cadastrados
        return {"eventos": []}, 200
    else:
        logger.debug(f"%d eventos econtrados" % len(eventos))
        # retorna a representação de evento
        return apresenta_eventos(eventos), 200


@app.get('/evento', tags=[evento_tag],
         responses={"200": EventoViewSchema, "404": ErrorSchema})
def get_evento(query: EventoBuscaSchema):
    """Faz a busca por um Evento a partir do id do evento

    Retorna uma representação dos eventos e pessoas associadas.
    """
    evento_id = query.id
    logger.debug(f"Coletando dados sobre evento #{evento_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    evento = session.query(Evento).filter(Evento.id == evento_id).first()

    if not evento:
        # se o evento não foi encontrado
        error_msg = "Evento não encontrado na base :/"
        logger.warning(f"Erro ao buscar evento '{evento_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Evento encontrado: '{evento.nome}'")
        # retorna a representação de evento
        return apresenta_evento(evento), 200


@app.delete('/evento', tags=[evento_tag],
            responses={"200": EventoDelSchema, "404": ErrorSchema})
def del_evento(query: EventoBuscaSchema):
    """Deleta um Evento a partir do id do evento informado

    Retorna uma mensagem de confirmação da remoção.
    """
    evento_id = query.id
    logger.debug(f"Deletando dados sobre evento #{evento_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Evento).filter(Evento.id == evento_id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado evento #{evento_id}")
        return {"mesage": "Evento removido", "id": evento_id}
    else:
        # se o evento não foi encontrado
        error_msg = "Evento não encontrado na base :/"
        logger.warning(f"Erro ao deletar evento #'{evento_id}', {error_msg}")
        return {"mesage": error_msg}, 404


@app.post('/pessoa', tags=[pessoa_tag],
          responses={"200": PessoaViewSchema, "404": ErrorSchema})
def add_pessoa(form: PessoaSchema):
    """Inscreve uma pessoa em um evento cadastrado na base identificado pelo id

    Retorna uma representação da pessoa inscrita.
    """
    evento_id = form.evento_id
    logger.debug(f"Adicionando pessoa ao evento #{evento_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca pelo evento
    evento = session.query(Evento).filter(Evento.id == evento_id).first()

    if not evento:
        # se evento não encontrado
        error_msg = "Evento não encontrado na base :/"
        logger.warning(f"Erro ao adicionar pessoa ao evento '{evento_id}', {error_msg}")
        return {"mesage": error_msg}, 404

    # criando a pessoa
    pessoa = Pessoa(
        nome=form.nome,
        email=form.email,
        evento_id=evento_id
    )

    # adicionando a pessoa ao evento
    evento.adiciona_pessoa(pessoa)
    session.commit()

    logger.debug(f"Adicionada pessoa ao evento #{evento_id}")

    # retorna a representação da pessoa
    return {
        "id": pessoa.id,
        "nome": pessoa.nome,
        "email": pessoa.email,
        "evento_id": pessoa.evento_id
    }, 200


@app.get('/eventos/categoria', tags=[evento_tag],
         responses={"200": ListagemEventosSchema})
def get_eventos_por_categoria(query: EventoBuscaCategoriaSchema):
    """Busca eventos por categoria

    Retorna uma representação da listagem de eventos.
    """
    categoria = query.categoria
    logger.debug(f"Coletando eventos da categoria '{categoria}'")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    eventos = session.query(Evento).filter(Evento.categoria == categoria).all()

    if not eventos:
        # se não há eventos cadastrados
        return {"eventos": []}, 200
    else:
        logger.debug(f"%d eventos econtrados" % len(eventos))
        # retorna a representação de evento
        return apresenta_eventos(eventos), 200
