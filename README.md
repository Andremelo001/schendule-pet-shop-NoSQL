# Schedule Pet Shop - Sistema de Agendamento

Sistema de agendamento para pet shop desenvolvido com FastAPI e MongoDB, oferecendo uma API RESTful completa para gerenciamento de clientes, pets, serviços e agendamentos.

## Funcionalidades

- **Gerenciamento de Clientes**: CRUD completo de clientes com suporte a permissões de administrador
- **Cadastro de Pets**: Registro de pets vinculados aos clientes
- **Catálogo de Serviços**: Gerenciamento de serviços com preço e duração
- **Sistema de Agendamentos**: Controle de agendamentos relacionando clientes, pets e serviços

## Tecnologias Utilizadas

- **[Python 3.12+](https://www.python.org/)** - Linguagem de programação
- **[FastAPI](https://fastapi.tiangolo.com/)** - Framework web moderno e de alta performance
- **[MongoDB](https://www.mongodb.com/)** - Banco de dados NoSQL
- **[Motor](https://motor.readthedocs.io/)** - Driver assíncrono para MongoDB
- **[Odmantic](https://art049.github.io/odmantic/)** - ODM (Object Document Mapper) para MongoDB
- **[Python-dotenv](https://pypi.org/project/python-dotenv/)** - Gerenciamento de variáveis de ambiente

## Pré-requisitos

Antes de começar, você precisará ter instalado:

- Python 3.12 ou superior
- MongoDB (local ou Atlas)
- pip (gerenciador de pacotes Python)
- uv (opcional, mas recomendado para gerenciamento de dependências)

## Instalação

1. **Clone o repositório**
```bash
git clone <url-do-repositorio>
cd schendule-pet-shop-NoSQL
```

2. **Crie e ative um ambiente virtual** (opcional, mas recomendado)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Instale as dependências**

Com uv:
```bash
uv sync
```

Ou com pip:
```bash
pip install -e .
```

## Configuração

1. **Crie um arquivo `.env` na raiz do projeto**
```bash
cp .env.example .env  # ou crie manualmente
```

2. **Configure as variáveis de ambiente no arquivo `.env`**
```env
url=mongodb://localhost:27017
# Para MongoDB Atlas:
# url=mongodb+srv://usuario:senha@cluster.mongodb.net/
```

## Como Executar

Execute o servidor de desenvolvimento:

```bash
fastapi dev app/main.py
```

O servidor estará disponível em `http://localhost:8000`

### Documentação Interativa da API

Após iniciar o servidor, acesse:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Diagrama de Classes

```mermaid
classDiagram
    direction LR
    class Client {
        name: str
        cpf: str
        age: int
        is_admin: bool
    }

    class Pet {
        name: str
        breed: str
        age: int
        size_in_centimeters: int
        id_client: int
    }

    class Schedule {
        date_schedule: date
        id_client: int
        id_pet: int
    }

    class Services {
        duration_in_minutes: int
        type_service: str
        price: float
    }

    Client "1" -- "*" Pet
    Client "1" -- "*" Schedule
    Schedule "*" --> "*" Services
    Schedule "*" -- "1" Pet
```