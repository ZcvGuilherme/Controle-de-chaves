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

## Instalação
  Clonar repositório
  ```bash
git clone https://github.com/ZcvGuilherme/Controle-de-chaves.git
  ```
Entrar na pasta
  ```bash
cd Controle-de-chaves
  ```

Criar ambiente virtual
```bash
python -m venv venv
```

Ativar ambiente
```bash
source venv/bin/activate  # Linux
venv\Scripts\activate     # Windows
```
Instalar dependências
```bash
pip install -r requirements.txt
```
Criar banco de dados
```bash
python manage.py migrate
```


