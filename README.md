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

cadastre pessoas na tabela Pessoa 
Verifique [Signals](#criar_usuario_para_pessoa)

Cadastre chaves na tabela Chaves
Verifique [Signals](#criar_status_automatico)


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
Quando uma pessoa é cadastrada no sistema, um usuário Django é criado automaticamente para autenticação.


### atualizar_usuario
Signal: post_save
Model: Pessoa
Sempre que os dados de uma pessoa são atualizados, o nome do usuário Django vinculado é sincronizado automaticamente.



