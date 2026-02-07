# 🔑 Sistema de Controle de Chaves

## 📖 Descrição

Sistema de controle e monitoramento de chaves desenvolvido durante a disciplina de **Extensão Curricular** do curso tecnólogo em **Análise e Desenvolvimento de Sistemas**.

O objetivo é gerenciar empréstimos, disponibilidade e responsabilidade sobre chaves institucionais, garantindo rastreabilidade e segurança no processo.

---

## 📑 Índice

* [Pré-requisitos](#-pré-requisitos)
* [Tecnologias](#-tecnologias-utilizadas)
* [Arquitetura](#-arquitetura)
* [Instalação](#-instalação)
* [Configuração básica](#-configuração-básica)
* [Funcionalidades extras](#funcionalidades-extras)
* [Modelagem do banco](#diagrama-entidade-relacionamento)
* [Signals](#-signals)

  * [criar_status_automatico](#criar_status_automatico)
  * [gerar_itembusca](#gerar_itembusca)
  * [criar_usuario_para_pessoa](#criar_usuario_para_pessoa)
  * [atualizar_usuario](#atualizar_usuario)
* [Estrutura do projeto](#estrutura-do-projeto)

---

## 📋 Pré-requisitos

* Python 3.12
* Git

---

## 🚀 Tecnologias Utilizadas

* **Backend:** Django 5
* **Banco de dados:** SQLite
* **Frontend:** DTL (Django Template Language), JavaScript e CSS

---

## 🏗️ Arquitetura

* **Backend:** Django (MVT — Model · View · Template)
* **ORM:** Nativo do Django
* **Banco atual:** SQLite
* **Frontend:** Templates + CSS + JS

---

# ⚙️ Instalação

### Clonar repositório

```bash
git clone https://github.com/ZcvGuilherme/Controle-de-chaves.git
```

### Entrar na pasta

```bash
cd Controle-de-chaves
```

### Criar ambiente virtual

```bash
python -m venv venv
```

### Ativar ambiente

```bash
source venv/bin/activate  # Linux
venv\Scripts\activate     # Windows
```

### Instalar dependências

```bash
pip install -r requirements.txt
```

### Criar banco de dados

```bash
python manage.py migrate
```

---

# 🔧 Configuração Básica

Crie um superusuário:

```bash
python manage.py createsuperuser
```

Inicie o servidor:

```bash
python manage.py runserver
```

Acesse o admin:

```
http://127.0.0.1:8000/admin
```

---

## 👤 Cadastro inicial

1. Cadastre pessoas na tabela **Pessoa**
2. Ajuste o atributo `must_change_password` se não quiser forçar redefinição no primeiro login

➡️ Verifique: [criar_usuario_para_pessoa](#criar_usuario_para_pessoa)

---

## 🔑 Cadastro de chaves

Cadastre chaves na tabela **Chave**.

➡️ Verifique: [criar_status_automatico](#criar_status_automatico)

Depois disso, faça as restrições de pessoa/chave conforme necessário.

# 🧩 Funcionalidades Extras

Além das funcionalidades principais, o sistema possui **comandos de gerenciamento e manutenção** que auxiliam na auditoria e segurança dos dados.

---

## 📊 Geração de relatório do histórico

Cria automaticamente um arquivo `.xlsx` contendo todos os registros da tabela **Histórico**.

### Comando

```bash
python manage.py gerar_relatorio
```

### Saída gerada

* Arquivo Excel (.xlsx)
* Contém:

  * Pessoa
  * Matrícula
  * Chave
  * Ação
  * Data
  * Hora

### Localização do comando

```
guarita/management/commands/gerar_relatorio.py
```

---

## 💾 Backup do banco de dados

Realiza o backup completo do banco atual do sistema.

### Comando

```bash
python manage.py dbbackup --clean
```

### Funções executadas

* Gera dump do banco
* Remove backups antigos (`--clean`)
* Mantém apenas versões recentes

### Observações

* Útil para rotinas de segurança
* Pode ser automatizado via CRON

---

# 🗄️ Diagrama entidade-relacionamento

<img width="600" height="400" alt="Diagrama ER" src="https://github.com/user-attachments/assets/eef82815-07ac-48c9-8f58-6dd67fa77894" />

---

# 🔔 Signals

O sistema utiliza **Django Signals** para automatizar regras de negócio e manter consistência entre entidades.

Localização:

```
guarita/signals.py
```

---

### criar_status_automatico

**Signal:** `post_save`
**Model:** `Chave`

Sempre que uma nova chave é cadastrada, o sistema cria automaticamente seu status na tabela **ChaveStatus**.

**Objetivo:** Garantir que toda chave possua controle de disponibilidade.

---

### gerar_itemBusca

**Signal:** `post_save`
**Model:** `Chave`

Após a criação de uma chave, é gerado automaticamente um identificador textual padronizado para buscas.

**Formato gerado:**

```
Chave <id> - <nome>
```

Exemplo:

```
Chave 12 - Laboratório de Redes
```

---

### criar_usuario_para_pessoa

**Signal:** `post_save`
**Model:** `Pessoa`

Quando uma pessoa é cadastrada, um usuário Django é criado automaticamente para autenticação.

**Regras:**

* Username = matrícula
* Senha inicial = matrícula ⚠️
* Nome sincronizado com `first_name`

> 🔒 **Importante:** Alterar política de senha em produção.

---

### atualizar_usuario

**Signal:** `post_save`
**Model:** `Pessoa`

Sempre que os dados da pessoa são atualizados, o nome do usuário vinculado é sincronizado automaticamente.

**Objetivo:** Manter consistência entre `Pessoa` e `auth.User`.

---

## 📚 Documentação completa

A documentação técnica detalhada do sistema foi gerada com **Sphinx**, contendo mais informações técnicas sobre o projeto.

Para acessá-la localmente, após gerar os arquivos HTML, abra o índice principal:

```bash
xdg-open docs/build/html/index.html
```

> 💡 O comando acima funciona em ambientes Linux com interface gráfica.
> Em outros sistemas, basta abrir manualmente o arquivo:

```
docs/build/html/index.html
```

Isso carregará a documentação navegável no navegador padrão.


---

# 🗂️ Estrutura do projeto

```
Controle-de-chaves/
│
├── README.md  
├── manage.py
├── requirements.txt
├── .gitignore
│
├── chaves/                    # Configurações do projeto Django
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── guarita/                   # App principal
│   ├── models.py
│   ├── views.py
│   ├── signals.py
│   ├── middleware.py
│   │
│   ├── management/commands/
│   │   └── gerar_relatorio.py
│   │
│   ├── services/
│   │   └── historico_service.py
│   │
│   ├── templates/
│   ├── static/
│   └── tests/
│
├── templates/                 # Templates globais
│   ├── base.html
│   └── componentes/
│
└── fixtures/                  # Dados iniciais
    ├── auth.json
    └── base.json
```

---

## 📌 Observações

* O banco atual é SQLite (dev).
* Pode ser migrado para PostgreSQL/MySQL em produção.
* Signals executam automaticamente após operações de save().

## 👥 Autores

### 👨‍💻 Guilherme Sousa

* GitHub: [https://github.com/ZcvGuilherme](https://github.com/ZcvGuilherme)
* LinkedIn: [https://www.linkedin.com/in/guisousas/](https://www.linkedin.com/in/guisousas/)
* Lattes: [https://lattes.cnpq.br/3242159995077179](https://lattes.cnpq.br/3242159995077179)
* Email: [guisousasilvanota10@email.com](mailto:guisousasilvanota10@email.com)

---

### 👨‍💻 John Victor Monção

* GitHub: [https://github.com/Nijoww](https://github.com/Nijoww)
* Email: [moncao099@gmail.com](moncao099@gmail.com)

---

### Waldeney Rodrigues Vieira

* GitHub: [https://github.com/Wal-dreamer](https://github.com/Wal-dreamer)
* Email: [walrvieira06@gmail.com](walrvieira06@gmail.com)

---

### Wellington Oliveira Carvalho
* GitHub: [https://github.com/Carvalhop2](https://github.com/Carvalhop2)
* Email: [wellingtonp2.oc@gmail.com](wellingtonp2.oc@gmail.com)
* Lattes: [https://lattes.cnpq.br/4590726252228745](https://lattes.cnpq.br/4590726252228745)
---

### Valfredo da Costa Silva
* GitHub: [https://github.com/valfredoDev](https://github.com/valfredoDev)
* Email: [valfredocosta.contato@gmail.com](valfredocosta.contato@gmail.com)
* Lattes: [https://lattes.cnpq.br/8187731285592440](https://lattes.cnpq.br/8187731285592440)
---

## 📜 Licença

Este projeto está sob a licença MIT.  
Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
