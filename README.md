# Sistema de Gestão de Posto de Combustível
Sistema web completo para gerenciamento de produtos, bombas de combustível, funcionários, empresa e usuários internos, desenvolvido com **Django 4**, **Class-Based Views**, **Mixins**, **Services Layer** e seguindo boas práticas do framework.

---

## 📌 📁 Sobre o Projeto
O objetivo é substituir controles manuais por um sistema centralizado, seguro e escalável, permitindo:

- Controle de usuários com diferentes níveis de permissão  
- Cadastro e gerenciamento da empresa  
- Gestão de produtos (combustíveis)  
- Controle de bombas e seus respectivos produtos  
- Cadastro de funcionários  
- Dashboard administrativo  
- Auditoria e logs de acesso  

O sistema segue o padrão Django e uma estrutura limpa que facilita manutenção e expansão.

---

## 🏗 Arquitetura Aplicada

O projeto utiliza:

### ✔ Class-Based Views (CBVs)
Organiza o fluxo das páginas usando herança, evitando duplicação e deixando o código mais limpo.

### ✔ Mixins
Criados para concentrar comportamentos comuns, como:
- Verificação de permissão por tipo de usuário  
- Controle de acesso  
- Regras de negócios compartilhadas  

Isso evita repetição de código e mantém o projeto modular.

### ✔ Services Layer
Camada responsável por regras de negócio que não pertencem diretamente à view nem ao model.  
Melhora a manutenção e evita views muito pesadas.

### ✔ Django ORM
Toda manipulação de banco é feita usando ORM, assegurando segurança e compatibilidade entre bancos de dados.

### ✔ Paginação, Filtros e Busca
Aplicados conforme recomendado nos requisitos não funcionais, principalmente em listagens de funcionários e produtos.

### ✔ Padrão de Pastas por Responsabilidade
O projeto segue a divisão clássica Django:

```text
app/
├── models.py
├── views.py
├── forms.py
├── filters.py
├── mixins.py
├── services.py
└── urls.py
```

---

## 🔒 Controle de Acesso
O sistema possui 3 perfis:

| Perfil           | Permissões                |
|------------------|---------------------------|
| **Administrador**| Acesso total              |
| **Gerente**      | Acesso aos cadastros e relatórios |
| **Operador**     | Somente consultas         |

Implementado com **PermissionRequiredMixin**, **UserPassesTestMixin** e mixins próprios, garantindo que:

- Operadores não acessem telas de criação/edição  
- Usuários inativos não consigam fazer login  
- Apenas administradores gerenciem usuários  

---

## 👤 Funcionalidades Principais

### 🔐 Autenticação e Usuários
- Tela de login com validação  
- Logout  
- Controle de acesso por perfil  
- CRUD completo de usuários (somente administrador)  

### 🏭 Cadastro da Empresa
- Edição única dos dados da empresa  
- Validação de CNPJ  
- Exibição dos dados em tela própria  

### ⛽ Produtos
- CRUD completo  
- Filtros e busca  
- Validação de preço de custo/venda  
- Estoque mínimo e estoque atual  
- Status (ativo/inativo)  

### 🛢 Bombas
- Relacionamento direto com produtos  
- Status (ativa, inativa, manutenção)  
- Filtros por produto e status  
- Exibição clara de qual produto está em cada bomba  

### 👨‍🔧 Funcionários
- CRUD completo  
- Validação de CPF  
- Paginação  
- Filtros por nome, cargo, status, etc.  
- Cálculo automático de tempo de empresa  

---

## 🧪 Testes Automatizados

O projeto contém testes para:

- Login  
- Regras de permissão  
- Usuários inativos  
- Regras de negócio críticas  

Para executar:

```bash
python manage.py test
```

---

## ⚙️ Instalação e Execução

### 1️⃣ Rodar o instalador automático

```bash
python configurar.py
```

Esse script:
- Cria o ambiente virtual  
- Instala as dependências  
- Aplica as migrations  

### 2️⃣ Ativar o ambiente virtual

PowerShell (Windows):

```bash
.\venv\Scripts\Activate.ps1
```

CMD (Windows):

```bash
venv\Scripts\activate
```

### 3️⃣ Rodar o servidor

```bash
python manage.py runserver
```

Acesse em:  
`http://127.0.0.1:8000/`

---

## 📊 Tecnologias Utilizadas

- Python 3.x  
- Django 4.x  
- Bootstrap 5  
- SQLite (desenvolvimento)  
- Django ORM  
- Django Filter  
- Mixins customizados  
- Services Layer  

---

## 📄 Licença

Projeto acadêmico / demonstrativo — livre para uso pessoal e estudos.

---

## 🙋 Autor

Desenvolvido por **Luis Guilherme Melo**, estagiário de desenvolvimento.

---


---
## README Original

# Sistema de Gestão de Posto de Combustível

Este é um sistema web desenvolvido em Python/Django.

### 1. Configuração Automática
Abra o terminal e digite:
```powershell
python configurar.py
```
*Este script vai criar o ambiente virtual, instalar as dependências e configurar o banco de dados para você.*

> **Importante:** o `configurar.py` roda `python manage.py makemigrations --check` antes de aplicar as migrações. Se ele detectar mudanças em `models.py` sem migrations, ele vai **avisar e parar**, pois gerar migrations automaticamente pode mascarar erros de versionamento.

### 2. Ativar o Ambiente e Rodar
Após a configuração terminar, use estes dois comandos:
```powershell
# Ativar o ambiente (comando específico para PowerShell)
.\venv\Scripts\Activate.ps1

# Rodar o servidor
python manage.py runserver
```
Acesse: `http://127.0.0.1:8000`

---


## 👤 Criar usuário ADMIN inicial (obrigatório para começar)

Depois de configurar, você precisa ter ao menos 1 usuário **ADMIN** para gerenciar usuários e cadastros.

### Comando (management command)
Com o ambiente virtual ativado:

```powershell
python manage.py createsuperuser
```

### Opção C: modo não-interativo (variáveis de ambiente)
Útil para automação/CI:

```powershell
$env:INITIAL_ADMIN_USERNAME="admin"
$env:INITIAL_ADMIN_EMAIL="admin@exemplo.com"
$env:INITIAL_ADMIN_NOME_COMPLETO="Administrador"
$env:INITIAL_ADMIN_PASSWORD="SenhaForte123"
python manage.py create_initial_admin --noinput
```


## 🛠 Solução de Problemas Comuns

### Erro de Permissão no PowerShell
Se ao tentar ativar o ambiente (`Activate.ps1`) você receber um erro de "Execução de Scripts", rode este comando no PowerShell como Administrador:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 🧪 Rodando testes

Com o ambiente ativado:

```powershell
python manage.py test
```

Existem testes básicos para:
- usuário **inativo** não conseguir logar;
- validação: **preço de venda não pode ser menor que o preço de custo**;
- validação de **CPF** e **CNPJ**.

## 📋 Funcionalidades
- Autenticação por perfis (Admin, Gerente, Operador).
- Gestão de Empresa, Produtos, Bombas e Funcionários.
- Interface com Bootstrap 5.
