# **InvestWise \- Analista de Investimentos com IA 📈**

**InvestWise** é uma plataforma inteligente que atua como um Analista de Investimentos Pessoal. Utilizando o poder do **Google Gemini**, o sistema analisa o perfil financeiro do usuário, cruza informações com tendências de mercado e gera recomendações de portfólio personalizadas, enviando relatórios detalhados por e-mail.

## **📋 Funcionalidades Principais**

O sistema opera através de uma orquestração de Agentes de IA:

* **🔍 Classificação de Perfil:** Analisa dados como renda, capital e objetivos para determinar se o investidor é Conservador, Moderado ou Arrojado.  
* **💡 Recomendação Inteligente:** Gera 3 opções de portfólio (com alocação percentual de ativos) baseadas no perfil identificado e em lógica de mercado.  
* **📧 Relatórios via E-mail:** Gera um template HTML responsivo e envia a análise completa para o usuário via SMTP (Gmail).  
* **⚡ Interface Reativa:** Feedback visual em tempo real, validação de formulários e modo escuro (Dark Mode).

## **🚀 Tecnologias Utilizadas**

O projeto foi construído utilizando uma arquitetura moderna separada em Frontend e Backend.

### **Frontend (Interface)**

* [**React**](https://react.dev/) \+ [**Vite**](https://vitejs.dev/): Para performance e construção rápida.  
* [**Tailwind CSS**](https://tailwindcss.com/): Para estilização responsiva e design system.  
* **Lucide React**: Biblioteca de ícones.

### **Backend (API & IA)**

* [**FastAPI**](https://fastapi.tiangolo.com/): Framework Python de alta performance para a API.  
* [**Google Generative AI**](https://ai.google.dev/): SDK do modelo **Gemini 2.5 Flash** para inteligência.  
* **SMTP Lib**: Para envio de e-mails transacionais.  
* **Pydantic**: Para validação rigorosa de dados.

## **📦 Como Rodar o Projeto**

Siga este guia passo a passo para configurar o ambiente localmente. Você precisará de dois terminais abertos.

### **Pré-requisitos**

* **Node.js** (v16+)  
* **Python** (v3.9+)  
* Uma chave de API do **Google Gemini**.  
* Uma **Senha de App** do Gmail (para envio de e-mails).

### **Passo 1: Configurando o Backend (Terminal 1\)**

1. Acesse a pasta do backend:  
   cd backend

2. Crie e ative o ambiente virtual (venv):  
   * **Windows:**  
     python \-m venv venv  
     .\\venv\\Scripts\\activate

   * **Mac/Linux:**  
     python3 \-m venv venv  
     source venv/bin/activate

3. Instale as dependências:  
   pip install \-r requirements.txt

4. 🔐 Configuração de Segurança (.env):  
   Crie um arquivo chamado .env dentro da pasta backend e preencha com seus dados:  
   \# backend/.env

   \# Sua chave da IA do Google  
   GEMINI\_API\_KEY=sua\_chave\_aqui\_sem\_aspas

   \# Configuração de E-mail (Necessário criar Senha de App no Google)  
   EMAIL\_ADDRESS=seu\_email@gmail.com  
   EMAIL\_PASSWORD=sua\_senha\_de\_app\_de\_16\_digitos

5. Inicie o servidor:  
   uvicorn main:app \--reload  
   O backend estará rodando em: http://127.0.0.1:8000

### **Passo 2: Configurando o Frontend (Terminal 2\)**

1. Abra um **novo terminal** na raiz do projeto e acesse a pasta frontend:  
   cd frontend

2. Instale as dependências do Node:  
   npm install

3. Inicie o servidor de desenvolvimento:  
   npm run dev

4. Acesse o projeto no seu navegador através do link exibido (geralmente http://localhost:5173).

## **📂 Estrutura do Projeto**

invest-wise/  
├── backend/  
│   ├── agentes\_ia.py    \# Lógica dos agentes (Classificador, Recomendador, Email)  
│   ├── main.py          \# API FastAPI (Rotas e Orquestração)  
│   ├── requirements.txt \# Dependências Python  
│   └── .env             \# Arquivo de segredos (NÃO COMMITAR)  
│  
└── frontend/  
    ├── src/  
    │   └── components/  \# Componentes React (InvestWiseApp.jsx)  
    ├── public/          \# Assets estáticos (Logo)  
    └── package.json     \# Dependências JS

## **🛡️ Notas de Segurança**

* O arquivo .gitignore já está configurado para **não enviar** arquivos .env ou pastas node\_modules e venv para o GitHub.  
* Nunca compartilhe sua GEMINI\_API\_KEY ou EMAIL\_PASSWORD publicamente.