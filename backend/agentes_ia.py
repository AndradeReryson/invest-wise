import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google import genai
from dotenv import load_dotenv
from pathlib import Path

# --- FORMA ROBUSTA DE CARREGAR .ENV ---
# Pega o caminho da pasta onde ESTE arquivo (agentes_ia.py) está
current_dir = Path(__file__).parent
# Aponta para o arquivo .env dentro dessa pasta
env_path = current_dir / '.env'
# Carrega explicitamente desse caminho
load_dotenv(dotenv_path=env_path)
# --------------------------------------

# 2. Recupera a chave e Inicializa o Client
api_key = os.getenv("GEMINI_API_KEY")
client = None

if api_key:
    # Nova forma de inicializar o cliente conforme documentação recente
    client = genai.Client(api_key=api_key)
else:
    print("⚠️ AVISO: Chave 'GEMINI_API_KEY' não encontrada no .env")


def fazer_classificacao(
    nome: str,
    email: str,
    renda: str,
    capital: str,
    finalidade: str,
    aporte_disponivel: str,
    enviarEmail: bool,
):
    """
    Agente Qualificador de Leads usando Gemini.
    Recebe dados do lead e retorna um JSON com Score e Recomendacao.
    """
    
    if not client:
        return {"error": "API Key não configurada ou Client não inicializado"}

    prompt = f"""
    Voce e um Gerente analista de investimentos Senior. Analise o lead abaixo e qualifique qual e o tipo de perfil desse lead.
    
    DADOS DO LEAD:
    Nome: {nome}
    E-mail: {email}
    Renda mensal: {renda}
    aporte disponivel: {aporte_disponivel}
    Capital: {capital}
    Finalidade: {finalidade}
    EnviarEmail: {enviarEmail}
        
    SAIDA OBRIGATORIA (JSON):
    {{
        "categoria": ("conservador", "moderado", "arrojado"),
        "e_investidor", ("sim","nao"),
        "resumo_analise": "Explicacao curta com base na sua analise",
        "nome": "nome"
        "email": "email"
        "renda_mensal": "renda"
        "aporte_disponivel": "aporte_disponivel"
        "capital": "capital"
        "finalidade": "finalidade"
        "enviarEmail": ("sim", "nao")
    }}
    Retorne APENAS o JSON valido, sem crase ou markdown.
    """

    try:
        # Nova sintaxe para geração de conteúdo
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        clean_text = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_text)
    except Exception as e:
        return {"error": str(e)}


def gerar_recomendacao(
    categoria: str,
    resumo_analise: str,
    e_investidor: str,
    nome: str,
    email: str,
    renda: str,
    capital: str,
    finalidade: str,
    aporte_disponivel: str,
    enviarEmail: str,
):
    """
    Agente Recomendador de Investimentos usando Gemini.
    """

    if not client:
        return {"error": "API Key não configurada ou Client não inicializado"}

    prompt = f"""
    Voce e um Gerente analista de investimentos Senior. \
    Analise o lead abaixo e com base nos seus conhecimentos e nas notícias do site <https://borainvestir.b3.com.br/> \
    Sugira três portfolios de investimento \
    A estrutura do atributo de saida sugestão é a seguinte: \
    sugestao: \
        portfolio 1: deve conter mais um objeto com cada opção de portfolio como um novo atributo (0, 1, 2 etc),\
        portfolio 2: deve conter mais um objeto com cada opção de portfolio como um novo atributo (0, 1, 2 etc),\
        portfolio 3: deve conter mais um objeto com cada opção de portfolio como um novo atributo (0, 1, 2 etc),\
    
    
    DADOS DO LEAD:
    categoria: {categoria}
    e_investidor: {e_investidor}
    resumo_analise: {resumo_analise}
    Nome: {nome}
    E-mail: {email}
    Renda mensal: {renda}
    aporte disponivel: {aporte_disponivel}
    Capital: {capital}
    Finalidade: {finalidade}
    EnviarEmail: {enviarEmail}

    A estrutura do atributo de saida sugestão deve ser a seguinte:
        
    SAIDA OBRIGATORIA (JSON):
    {{
        "nome": "nome",
        "email": "email",
        "sugestao": "sugestao"
        "resumo_analise": "Explicacao curta com base na sua analise",
        "enviarEmail": "enviarEmail"
    }}
    Retorne APENAS o JSON valido, sem crase ou markdown.
    """

    try:
        # Nova sintaxe para geração de conteúdo
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        clean_text = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_text)
    except Exception as e:
        return {"error": str(e)}


def gerar_email_template(
    nome: str, email: str, sugestao: object, resumo_analise: str, enviarEmail: str
):
    """
    Agente Gerador de Template HTML para E-mail.
    """
    
    if not client:
        return {"error": "API Key não configurada ou Client não inicializado"}

    html_content = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Recomendação InvestWise</title>
        <!-- Importando Montserrat para clientes que suportam -->
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');
        </style>
    </head>
    <body style="margin: 0; padding: 0; background-color: #191414; font-family: 'Montserrat', Arial, sans-serif; color: #FAF9F6;">
        
        <!-- Container Principal Centralizado -->
        <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #191414;">
            <tr>
                <td align="center" style="padding: 20px;">
                    
                    <!-- Caixa de Conteúdo (Max 600px) -->
                    <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px; background-color: #100c0c; border-radius: 8px; overflow: hidden; border: 1px solid #333333;">
                        
                        <!-- 1. CABEÇALHO COM LOGO -->
                        <tr>
                            <td align="center" style="padding: 40px 20px; background-color: #100c0c; border-bottom: 1px solid #333;">
                                <!-- Substitua o src abaixo pela URL pública da sua logo hospedada -->
                                <!-- Ex: https://seu-bucket.com/SIMBOLO_BIG.png -->
                                <div style="font-family: 'Montserrat', sans-serif;">
                                    <span style="font-size: 28px; font-weight: bold; color: #1DB954; letter-spacing: -1px;">INVEST</span>
                                    <br>
                                    <span style="font-size: 24px; font-weight: 300; color: #FFFFFF; letter-spacing: 4px; text-transform: uppercase;">WISE</span>
                                </div>
                            </td>
                        </tr>

                        <!-- 2. SAUDAÇÃO E RESUMO -->
                        <tr>
                            <td style="padding: 40px 30px;">
                                <h1 style="margin: 0 0 20px 0; font-size: 24px; color: #FFFFFF;">
                                    Prezado(a) <span style="color: #1DB954;">{{ nome }}</span>,
                                </h1>
                                <p style="margin: 0 0 30px 0; font-size: 16px; line-height: 1.6; color: #CCCCCC; text-align: justify;">
                                    {{ resumo_analise }}
                                </p>

                                <hr style="border: 0; border-top: 1px solid #333333; margin: 30px 0;">

                                <!-- TÍTULO DA SEÇÃO -->
                                <h2 style="margin: 0 0 25px 0; font-size: 20px; color: #1ED760; text-transform: uppercase; letter-spacing: 1px;">
                                    Sugestões de Portfólio
                                </h2>

                                <!-- 3. BLOCO DE PORTFÓLIOS (LOOP) -->
                                <!-- 
                                    DICA PARA O WINDMILL: 
                                    No seu script, você provavelmente iterará sobre o objeto 'sugestao'.
                                    O bloco abaixo representa UM portfólio. Repita essa estrutura para cada item.
                                -->
                                
                                <!-- INICIO DO ITEM DE PORTFÓLIO -->
                                <div style="background-color: #2a2a2a; border-left: 4px solid #1DB954; padding: 20px; margin-bottom: 20px; border-radius: 4px;">
                                    <h3 style="margin: 0 0 15px 0; font-size: 18px; color: #1ED760;">
                                        {{ nome_do_portfolio }} <!-- Ex: Portfólio 1: Conservador -->
                                    </h3>
                                    
                                    <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">
                                        <!-- INICIO DO ITEM DA LISTA (LOOP INTERNO) -->
                                        <tr>
                                            <td valign="top" style="width: 20px; padding-top: 5px;">
                                                <span style="display: block; width: 8px; height: 8px; background-color: #FFFFFF; border-radius: 50%;"></span>
                                            </td>
                                            <td style="padding-bottom: 10px; font-size: 14px; color: #E0E0E0; line-height: 1.5;">
                                                {{ item_do_portfolio }} <!-- Ex: Tesouro Direto: 70% do aporte... -->
                                            </td>
                                        </tr>
                                        <!-- FIM DO ITEM DA LISTA -->
                                        
                                        <!-- (Repita a estrutura <tr> acima para outros itens se não estiver usando loop no template) -->
                                    </table>
                                </div>
                                <!-- FIM DO ITEM DE PORTFÓLIO -->

                            </td>
                        </tr>

                        <!-- 4. FOOTER / DISCLAIMER -->
                        <tr>
                            <td align="center" style="padding: 30px; background-color: #000000; border-top: 1px solid #333;">
                                <p style="margin: 0; font-size: 12px; color: #666666; letter-spacing: 1px; text-transform: uppercase;">
                                    INVESTWISE • IA FINANCEIRA
                                </p>
                                <p style="margin: 10px 0 0 0; font-size: 10px; color: #444444; line-height: 1.4;">
                                    Este é um relatório gerado automaticamente por Inteligência Artificial.<br>
                                    As sugestões não constituem garantia de rentabilidade.
                                </p>
                            </td>
                        </tr>

                    </table>
                    
                    <!-- Espaço Extra no Final -->
                    <div style="height: 40px;"></div>

                </td>
            </tr>
        </table>

    </body>
    </html>
    """

    prompt = f"""
    Voce faz parte da equipe de marketing da empresa InvestWise \
    Seus colegas de equipe já fizeram a analise dos dados do cliente e criaram três portfolios de investimento para um cliente \
    Sua missão é preencher o código HTML do email para que ele contenha todas as informações. \
    Importante: o campo de sugestão dos dados do cliente é um objeto com os três portfolios que possuem mais objetos dentro, seguindo a seguinte lógica \
    sugestao: \
        portfolio 1: deve conter mais um objeto com cada opção de portfolio como um novo atributo (0, 1, 2 etc),\
        portfolio 2: deve conter mais um objeto com cada opção de portfolio como um novo atributo (0, 1, 2 etc),\
        portfolio 3: deve conter mais um objeto com cada opção de portfolio como um novo atributo (0, 1, 2 etc).\
    Tendo isso em vista, preencha o código HTML definido na variável 'html_content'

    
    
    DADOS DO USUARIO A SEREM PREENCHIDOS NO TEMPLATE HTML E USADOS PARA ENVIO DO EMAIL:
    Nome: {nome}
    Email: {email}
    Sugestao: {sugestao}
    Resumo_analise: {resumo_analise}
    EnviarEmail: {enviarEmail}
    Template_HTML: {html_content} 

    SAIDA OBRIGATORIA (JSON):
    {{
        "nome": "nome",
        "email": "email",
        "assunto_email": "assunto para ser colocado no email, se certificando que a codificação do texto esteja correta (UTF=8) e compatível com os sistemas de email"
        "html_template": "codigo HTML preenchido com os dados necessários"
    }}
    Retorne APENAS o JSON valido, sem crase ou markdown.
    """

    try:
        # Nova sintaxe para geração de conteúdo
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        clean_text = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_text)
    except Exception as e:
        return {"error": str(e)}


# --- NOVA FUNÇÃO: ENVIO REAL DE E-MAIL ---
def enviar_email_real(destinatario: str, assunto: str, html_content: str):
    """
    Envia o e-mail usando SMTP do Gmail (ou outro provedor).
    Requer variáveis EMAIL_ADDRESS e EMAIL_PASSWORD no .env
    """
    remetente = os.getenv("EMAIL_ADDRESS")
    senha = os.getenv("EMAIL_PASSWORD")
    
    if not remetente or not senha:
        print("❌ Erro: Credenciais de e-mail não configuradas no .env")
        return False

    try:
        # Configuração da mensagem
        msg = MIMEMultipart()
        msg['From'] = remetente
        msg['To'] = destinatario
        msg['Subject'] = assunto

        # Anexa o HTML
        msg.attach(MIMEText(html_content, 'html'))

        # Conexão com Servidor SMTP (Exemplo Gmail)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls() # Criptografia
        server.login(remetente, senha)
        text = msg.as_string()
        server.sendmail(remetente, destinatario, text)
        server.quit()
        
        print(f"✅ E-mail enviado com sucesso para {destinatario}")
        return True
        
    except Exception as e:
        print(f"❌ Falha ao enviar e-mail: {str(e)}")
        return False


def main():
    print("Arquivo de agentes carregado. Execute main.py para rodar a API.")

if __name__ == "__main__":
    main()