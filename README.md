# Evento App API

API REST para cadastro e gerenciamento de eventos, com suporte a inscrição de participantes.

## Tecnologias

- Python 3
- Flask (via flask-openapi3)
- SQLite
- SQLAlchemy

## Como executar

### 1. Criar e ativar o ambiente virtual

```bash
python -m venv env
```

Windows:
```bash
env\Scripts\activate
```

Linux/Mac:
```bash
source env/bin/activate
```

### 2. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 3. Executar a API

```bash
flask run --host 0.0.0.0 --port 5000
```

A API estará disponível em `http://127.0.0.1:5000`.

### 4. Documentação (Swagger)

Acesse `http://127.0.0.1:5000/openapi` para visualizar a documentação interativa da API.

## Rotas disponíveis

| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/evento` | Cadastrar novo evento |
| GET | `/eventos` | Listar todos os eventos |
| GET | `/evento` | Buscar evento por ID |
| DELETE | `/evento` | Remover evento por ID |
| POST | `/pessoa` | Inscrever pessoa em um evento |
| GET | `/eventos/categoria` | Filtrar eventos por categoria |
