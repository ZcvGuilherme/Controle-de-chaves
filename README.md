# Sistema de Controle de Chaves

## Descrição
  Este é um sistema de controle e monitoramento de chaves desenvolvido durante a disciplina de extensão curricular do curso tecnólogo de Análise e Desenvolvimento de Sistemas. 
  
## Pré-Requisitos
  - Python 3.12
  - Git
    
## Tecnologias Utilizadas
  - Django 5
  - SQlite
  - JavaScript/CSS

## Arquitetura
  - Backend: Django – Modelo MVT (Model - View - Template) e JS
  - Banco de dados: ORM do django, configurado atualmente com SQlite.
  - Frontend: DTL(Django Template Language)/CSS

# Instalação
#### Clonar repositório
  ```bash
git clone https://github.com/ZcvGuilherme/Controle-de-chaves.git
  ```
#### Entrar na pasta
  ```bash
cd Controle-de-chaves
  ```

#### Criar ambiente virtual
```bash
python -m venv venv
```

#### Ativar ambiente
```bash
source venv/bin/activate  # Linux
venv\Scripts\activate     # Windows
```
#### Instalar dependências
```bash
pip install -r requirements.txt
```
#### Criar banco de dados
```bash
python manage.py migrate
```

# Configuração Básica
Após a instalação, crie um superusuário com o seguinte comando: 
```bash
python manage.py createsuperuser
```

Logo após, abra o servidor com:
```bash
python manage.py runserver
```
Acesse a url e faça login com o superusuário:
http://127.0.0.1:8000/admin

Cadastre pessoas na tabela Pessoa. Altere o atributo must_change_password caso não queira ser redirecionado à tela de redefinição de senha no primeiro uso.

Verifique [Signals](#criar_usuario_para_pessoa)


Cadastre chaves na tabela Chaves
Verifique [Signals](#criar_status_automatico)

Faça as restrições de pessoas/chave caso necessário.


## Diagrama entidade-relacionamento:
<img width="600" height="400" alt="chaves_database (1)" src="https://github.com/user-attachments/assets/eef82815-07ac-48c9-8f58-6dd67fa77894" />

Configurações em guarita/signals

### criar_status_automatico
Signal: post_save
Model: Chave
Sempre que uma nova chave é cadastrada, o sistema cria automaticamente seu status de controle na tabela ChaveStatus.


### gerar_itemBusca
Signal: post_save
Model: Chave
Após a criação de uma chave, é gerado automaticamente um identificador textual padronizado para facilitar buscas no sistema.


### criar_usuario_para_pessoa
Signal: post_save
Model: Pessoa
Quando uma pessoa é cadastrada no sistema, um usuário Django é criado automaticamente para autenticação. A senha inicial é igual à matrícula (deve ser alterada em produção).


### atualizar_usuario
Signal: post_save
Model: Pessoa
Sempre que os dados de uma pessoa são atualizados, o nome do usuário Django vinculado é sincronizado automaticamente.


## Estrutura do projeto

```
Controle-de-chaves/
│
├── README.md  
├── manage.py
├── requirements.txt
├── .gitignore
│
├── chaves/                    # Configurações principais do projeto Django
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── guarita/                   # App principal do sistema
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── middleware.py
│   ├── models.py
│   ├── signals.py
│   ├── urls.py
│   ├── views.py
│   │
│   ├── migrations/
│   │   └── *.py
│   │
│   ├── management/
│   │   └── commands/
│   │       └── gerar_relatorio.py
│   │
│   ├── services/
│   │   └── historico_service.py
│   │
│   ├── templates/
│   │   ├── change_password.html
│   │   ├── status_chaves.html
│   │   └── registration/
│   │       └── login.html
│   │
│   ├── static/
│   │   └── login/
│   │       └── style.css
│   │
│   └── tests/
│       ├── models/
│       │   ├── test_busca.py
│       │   ├── test_insert.py
│       │   └── test_update.py
│       └── views/
│           ├── test_busca.py
│           └── test_page_exists.py
│
├── templates/                 # Templates globais
│   ├── base.html
│   │
│   ├── componentes/
│   │   ├── botao.html
│   │   ├── chave_item.html
│   │   ├── filtro_chaves.html
│   │   └── lista_chaves.html
│   │
│   └── static/
│       ├── style.css
│       ├── scripts.js
│       └── img/
│           ├── FAVICONCTCHAVE.png
│           ├── key-disponivel.png
│           ├── key-indisponivel.png
│           └── logoIfpi.png
│
└── fixtures/                  # Dados iniciais
    ├── auth.json
    └── base.json
```
