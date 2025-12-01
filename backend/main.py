from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pathlib import Path
import agentes_ia # Importa seu arquivo de agentes

# Carrega ambiente
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

app = FastAPI(title="InvestWise API")

# CORS (Permite conexão do React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de entrada (tem que bater com o JSON do React)
class UserData(BaseModel):
    nome: str
    email: str
    renda: str
    capital: str
    finalidade: str
    aporte_disponivel: str
    enviarEmail: bool

@app.post("/gerar-recomendacao")
async def processar_investimento(data: UserData):
    print(f"🚀 Iniciando processamento para: {data.nome}")
    
    try:
        # ---------------------------------------------------------
        # PASSO 1: CLASSIFICAÇÃO (Agente 1)
        # ---------------------------------------------------------
        print("1️⃣ Classificando perfil...")
        dados_classificacao = agentes_ia.fazer_classificacao(
            nome=data.nome,
            email=data.email,
            renda=data.renda,
            capital=data.capital,
            finalidade=data.finalidade,
            aporte_disponivel=data.aporte_disponivel,
            enviarEmail=data.enviarEmail
        )
        
        # Extrai dados importantes do retorno do agente 1
        categoria = dados_classificacao.get("categoria", "moderado")
        resumo = dados_classificacao.get("resumo_analise", "")
        # Supondo que o agente retorna "e_investidor"
        e_investidor = dados_classificacao.get("e_investidor", "nao") 

        # ---------------------------------------------------------
        # PASSO 2: RECOMENDAÇÃO (Agente 2)
        # ---------------------------------------------------------
        print(f"2️⃣ Gerando recomendação para perfil {categoria}...")
        dados_recomendacao = agentes_ia.gerar_recomendacao(
            categoria=categoria,
            resumo_analise=resumo,
            e_investidor=e_investidor,
            nome=data.nome,
            email=data.email,
            renda=data.renda,
            capital=data.capital,
            finalidade=data.finalidade,
            aporte_disponivel=data.aporte_disponivel,
            enviarEmail=str(data.enviarEmail) # Convertendo bool para str se o prompt pedir
        )

        sugestao_portfolios = dados_recomendacao.get("sugestao", {})

        # ---------------------------------------------------------
        # PASSO 3: E-MAIL (Agente 3 + Envio Real)
        # ---------------------------------------------------------
        if data.enviarEmail:
            print("3️⃣ Gerando template e enviando e-mail...")
            
            # 3.1 Gera o HTML preenchido
            dados_email = agentes_ia.gerar_email_template(
                nome=data.nome,
                email=data.email,
                sugestao=sugestao_portfolios,
                resumo_analise=resumo,
                enviarEmail=str(data.enviarEmail)
            )
            
            assunto = dados_email.get("assunto_email", "Sua Recomendação InvestWise")
            html_final = dados_email.get("html_template", "")

            # 3.2 Envia de verdade usando SMTP
            if html_final:
                agentes_ia.enviar_email_real(
                    destinatario=data.email,
                    assunto=assunto,
                    html_content=html_final
                )
            else:
                print("⚠️ HTML do email veio vazio, pulando envio.")

        # Retorna o resultado final para o Front-end mostrar na tela
        return dados_recomendacao

    except Exception as e:
        print(f"❌ Erro crítico: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Para rodar: uvicorn main:app --reload