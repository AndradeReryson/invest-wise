# **InvestWise \- Analista de Investimentos com IA**

**InvestWise** é uma plataforma inteligente que utiliza agentes de Inteligência Artificial para analisar o perfil financeiro do usuário e sugerir portfólios de investimento personalizados, baseados em tendências de mercado e objetivos pessoais.

## **📋 Sobre o Projeto**

O sistema atua como um "Analista de Investimentos Digital". Através de uma interface moderna e intuitiva, o usuário fornece seus dados financeiros e objetivos. O sistema então se comunica com um backend de automação (Windmill) onde agentes de IA processam essas informações, cruzam com dados de mercado e retornam estratégias de alocação de ativos otimizadas.

### **Principais Características**

* **Análise de Perfil:** Coleta dados como renda, capital disponível e finalidade do investimento.  
* **Processamento em Tempo Real:** Feedback visual enquanto a IA processa os dados (Loading State).  
* **Recomendações Personalizadas:** Sugestão de múltiplos portfólios (Conservador, Moderado, Arrojado, etc.) com alocação percentual.  
* **Integração com E-mail:** Opção para receber o relatório completo na caixa de entrada.

## **🚀 Tecnologias Utilizadas**

O projeto foi desenvolvido utilizando as tecnologias mais modernas do ecossistema React:

* [**React**](https://react.dev/) (via [**Vite**](https://vitejs.dev/)): Para construção da interface reativa e performática.  
* [**Tailwind CSS**](https://tailwindcss.com/): Para estilização rápida, responsiva e moderna.  
* [**Lucide React**](https://lucide.dev/): Biblioteca de ícones leves e consistentes.  
* [**Windmill**](https://www.windmill.dev/): Plataforma de scripts e fluxos de trabalho para o backend da IA.

## **📦 Como Executar o Projeto**

Siga os passos abaixo para rodar o InvestWise no seu ambiente local.

### **Pré-requisitos**

* **Node.js** instalado (versão 16 ou superior).  
* Um token de acesso válido para a API do Windmill (Workflow invest\_wise\_workflow).

### **Passo a Passo**

1. **Clone o repositório:**  
   git clone \[https://github.com/seu-usuario/invest-wise.git\](https://github.com/seu-usuario/invest-wise.git)  
   cd invest-wise

2. **Instale as dependências:**  
   npm install

3. Configure as Variáveis de Ambiente:  
   Crie um arquivo .env na raiz do projeto (baseado no exemplo abaixo) e adicione seu token de API.  
   *Arquivo .env:*  
   VITE\_API\_TOKEN=seu\_token\_do\_windmill\_aqui

4. **Inicie o Servidor de Desenvolvimento:**  
   npm run dev

5. Acesse o Projeto:  
   Abra seu navegador em http://localhost:5173.

## **🔧 Configuração de Proxy (CORS)**

Para evitar erros de **CORS** (Cross-Origin Resource Sharing) durante o desenvolvimento local ao comunicar-se com o Windmill, este projeto utiliza um proxy configurado no vite.config.js.

As chamadas para /windmill-proxy são redirecionadas automaticamente para https://app.windmill.dev, garantindo uma comunicação segura e fluida entre o frontend local e a API externa.

## **📱 Layout e Design**

O projeto segue um design **Mobile-First** e totalmente responsivo:

* **Desktop:** Layout em *Split-Screen* (Formulário à esquerda, Conteúdo visual à direita).  
* **Mobile:** Menu lateral (Sidebar) acessível via botão "hambúrguer" e interface adaptada para telas verticais.  
* **Tema:** Paleta de cores escura (*Dark Mode*) com acentos em Verde InvestWise (\#1DB954).

## **📄 Licença**

Este projeto está sob a licença MIT. Sinta-se à vontade para contribuir\!

Desenvolvido com 💚 por \[Seu Nome\]