import React, { useState, useEffect, useRef } from 'react';
import { Send, CheckCircle, AlertCircle, Menu, X, ArrowUpRight, XCircle } from 'lucide-react';

/**
 * CORES DO PROJETO:
 * Green: #1DB954
 * Malachite: #1ED760
 * Chinese Black: #191414
 * Off-white: #FAF9F6
 */

const InvestWiseApp = () => {
  // --- ESTADOS ---
  const [formData, setFormData] = useState({
    nome: '',
    email: '',
    renda: '',
    capital: '',
    aporte: '',
    finalidade: '',
    enviarEmail: false
  });

  const [viewState, setViewState] = useState('initial'); // 'initial', 'loading', 'result'
  const [apiResult, setApiResult] = useState(null);
  const [errorMsg, setErrorMsg] = useState(null); 
  const [showMobileMenu, setShowMobileMenu] = useState(false);
  const resultRef = useRef(null);

  // --- CONFIGURAÇÃO DA API LOCAL (FastAPI) ---
  // Aponta para o seu backend Python rodando localmente
  const API_URL = "http://localhost:8000/gerar-recomendacao";

  // --- EFEITOS DE UI (Favicon e Título) ---
  useEffect(() => {
    document.title = "InvestWise";
    let link = document.querySelector("link[rel~='icon']");
    if (!link) {
      link = document.createElement('link');
      link.rel = 'icon';
      document.getElementsByTagName('head')[0].appendChild(link);
    }
    link.href = 'SIMBOLO_BIG.png';
  }, []);

  // --- HANDLERS ---
  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMsg(null); 
    setViewState('loading');
    setShowMobileMenu(false);

    console.group("🚀 Iniciando Comunicação com API Local");

    try {
      console.log("Enviando dados para:", API_URL);
      
      // Chamada direta para o seu backend Python
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
          "Content-Type": "application/json",
          // Não precisamos de Authorization aqui pois o backend local gerencia as chaves
        },
        body: JSON.stringify({
            nome: formData.nome,
            email: formData.email,
            renda: formData.renda,
            capital: formData.capital,
            finalidade: formData.finalidade,
            // Mapeando o campo do form 'aporte' para o esperado 'aporte_disponivel' do Python
            aporte_disponivel: formData.aporte, 
            enviarEmail: formData.enviarEmail
        })
      });

      if (!response.ok) {
          const errorText = await response.text();
          throw new Error(`Erro na API (${response.status}): ${errorText}`);
      }

      const data = await response.json();
      console.log("✅ Resposta recebida:", data);

      // Atualiza a tela com o resultado
      setApiResult(data);
      setViewState('result');

    } catch (error) {
      console.error("❌ ERRO NO PROCESSO:", error);
      setErrorMsg(error.message || "Erro ao conectar com o servidor local. Verifique se o backend está rodando.");
      setViewState('initial'); 
    } finally {
      console.groupEnd();
    }
  };

  // --- RENDERIZADORES ---

  return (
    <div className="flex flex-col md:flex-row h-screen bg-[#191414] font-montserrat text-[#FAF9F6] overflow-hidden">
      
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');
        .font-montserrat { font-family: 'Montserrat', sans-serif; }
        .dot-flashing {
          position: relative;
          width: 15px;
          height: 15px;
          border-radius: 10px;
          background-color: #FAF9F6;
          color: #FAF9F6;
          animation: dot-flashing 1s infinite linear alternate;
          animation-delay: 0.5s;
        }
        .dot-flashing::before, .dot-flashing::after {
          content: '';
          display: inline-block;
          position: absolute;
          top: 0;
        }
        .dot-flashing::before {
          left: -25px;
          width: 15px;
          height: 15px;
          border-radius: 10px;
          background-color: #FAF9F6;
          color: #FAF9F6;
          animation: dot-flashing 1s infinite alternate;
          animation-delay: 0s;
        }
        .dot-flashing::after {
          left: 25px;
          width: 15px;
          height: 15px;
          border-radius: 10px;
          background-color: #FAF9F6;
          color: #FAF9F6;
          animation: dot-flashing 1s infinite alternate;
          animation-delay: 1s;
        }
        @keyframes dot-flashing {
          0% { background-color: #FAF9F6; transform: scale(1); }
          50%, 100% { background-color: rgba(250, 249, 246, 0.2); transform: scale(0.5); }
        }
        .curtain-exit { animation: curtain-up 1.2s cubic-bezier(0.77, 0, 0.175, 1) forwards; }
        @keyframes curtain-up { 0% { height: 100%; top: 0; } 100% { height: 60px; top: 0; } }
        .fade-in { animation: fadeIn 0.8s ease-in; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        
        /* Scrollbar */
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: #191414; }
        ::-webkit-scrollbar-thumb { background: #333; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #1DB954; }
      `}</style>

      {/* --- SIDEBAR --- */}
      <div className={`
        fixed inset-0 z-20 bg-[#191414] p-8 transition-transform duration-300 md:relative md:w-1/3 md:translate-x-0 md:border-r md:border-gray-800 h-full overflow-y-auto
        ${showMobileMenu ? 'translate-x-0' : '-translate-x-full'}
      `}>
        <div className="flex flex-col min-h-min">
          <div className="mb-10 flex items-center gap-3">
             <div className="w-16 h-16 relative">
                 <img 
                    src="SIMBOLO_BIG.png" 
                    alt="InvestWise Logo" 
                    className="object-contain w-full h-full drop-shadow-[0_0_10px_rgba(29,185,84,0.5)]"
                    onError={(e) => {e.target.style.display='none'; e.target.nextSibling.style.display='flex'}}
                 />
                 <div className="hidden absolute inset-0 bg-transparent border-2 border-[#1DB954] rounded-full items-center justify-center text-[#1DB954]">
                    <ArrowUpRight size={32} />
                 </div>
             </div>
             <div>
                 <h1 className="text-3xl font-bold tracking-tighter text-[#1DB954]">INVEST</h1>
                 <h1 className="text-3xl font-light tracking-[0.2em] text-white -mt-2">WISE</h1>
             </div>
          </div>

          <form onSubmit={handleSubmit} className="flex flex-col gap-5 flex-grow pb-4">
            <div>
              <label className="block text-sm font-semibold mb-2">Nome *</label>
              <input required name="nome" value={formData.nome} onChange={handleInputChange} className="w-full bg-white text-black p-3 rounded-md focus:outline-none focus:ring-2 focus:ring-[#1DB954]" placeholder="Seu nome completo" />
            </div>
            <div>
              <label className="block text-sm font-semibold mb-2">Email</label>
              <input type="email" name="email" value={formData.email} onChange={handleInputChange} className="w-full bg-white text-black p-3 rounded-md focus:outline-none focus:ring-2 focus:ring-[#1DB954]" placeholder="seu@email.com" />
            </div>
            <div>
              <label className="block text-sm font-semibold mb-2">Renda *</label>
              <input required name="renda" value={formData.renda} onChange={handleInputChange} className="w-full bg-white text-black p-3 rounded-md focus:outline-none focus:ring-2 focus:ring-[#1DB954]" placeholder="R$ 0,00" />
            </div>
            <div>
              <label className="block text-sm font-semibold mb-2">Capital Total *</label>
              <input required name="capital" value={formData.capital} onChange={handleInputChange} className="w-full bg-white text-black p-3 rounded-md focus:outline-none focus:ring-2 focus:ring-[#1DB954]" placeholder="R$ 0,00" />
            </div>
            <div>
              <label className="block text-sm font-semibold mb-2">Aporte Disponível *</label>
              <input required name="aporte" value={formData.aporte} onChange={handleInputChange} className="w-full bg-white text-black p-3 rounded-md focus:outline-none focus:ring-2 focus:ring-[#1DB954]" placeholder="R$ 0,00" />
            </div>
            <div>
              <label className="block text-sm font-semibold mb-2">Finalidade (Motivo de Investir) *</label>
              <textarea required name="finalidade" value={formData.finalidade} onChange={handleInputChange} rows={4} className="w-full bg-white text-black p-3 rounded-md focus:outline-none focus:ring-2 focus:ring-[#1DB954] resize-none" placeholder="Ex: Aposentadoria..." />
            </div>
            <div className="flex items-center gap-3 mt-2">
               <label className="relative inline-flex items-center cursor-pointer">
                <input type="checkbox" name="enviarEmail" checked={formData.enviarEmail} onChange={handleInputChange} className="sr-only peer" />
                <div className="w-11 h-6 bg-gray-600 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-[#1DB954] rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-[#1DB954]"></div>
                <span className="ml-3 text-sm font-medium text-gray-300">Receber no E-Mail</span>
              </label>
            </div>
            
            {errorMsg && (
                <div className="bg-red-500/20 border border-red-500 text-red-200 p-3 rounded flex items-start gap-2 text-sm animate-pulse">
                    <AlertCircle size={16} className="mt-0.5 min-w-[16px]" />
                    <span>{errorMsg}</span>
                </div>
            )}

            <button type="submit" disabled={viewState === 'loading'} className="mt-6 w-full bg-[#1DB954] hover:bg-[#1ED760] text-black font-bold py-4 rounded-md transition-colors flex items-center justify-center gap-2 uppercase tracking-wide disabled:opacity-50 disabled:cursor-not-allowed">
               {viewState === 'loading' ? 'Processando IA...' : 'Gerar Recomendação'}
            </button>
          </form>
        </div>
      </div>

      <button className="md:hidden fixed top-4 left-4 z-50 text-white bg-[#191414] p-2 rounded-md border border-[#1DB954]" onClick={() => setShowMobileMenu(!showMobileMenu)}>
        {showMobileMenu ? <X /> : <Menu />}
      </button>

      {/* --- MAIN CONTENT AREA --- */}
      <div className="relative flex-1 bg-black h-full overflow-hidden">
        
        {viewState === 'initial' && (
             <div className="absolute inset-0 flex flex-col justify-center items-center p-10 text-center bg-[#100c0c]">
                <div className="max-w-2xl fade-in">
                    <h2 className="text-[#1DB954] text-xl font-bold tracking-widest mb-4 uppercase">Analista de Investimentos Personalizado!</h2>
                    <h1 className="text-4xl md:text-6xl font-bold text-white mb-8 leading-tight">Comece a investir com <span className="text-[#1DB954] decoration-wavy underline">segurança</span>!</h1>
                    <p className="text-gray-400 text-lg md:text-xl leading-relaxed">Nosso agente de IA pesquisa e recomenda portfólios de investimento diversificados de acordo com seu perfil financeiro e objetivos de vida.</p>
                </div>
            </div>
        )}

        {(viewState === 'loading' || viewState === 'result') && (
            <div className={`absolute inset-0 z-30 bg-[#1DB954] flex flex-col items-center justify-center transition-all duration-1000 ${viewState === 'result' ? 'curtain-exit' : ''}`}>
                {viewState === 'loading' && (
                    <div className="text-center">
                        <div className="dot-flashing mx-auto mb-8"></div>
                        <h2 className="mt-8 text-[#191414] font-bold text-2xl tracking-widest uppercase animate-pulse">Analisando Mercado...</h2>
                    </div>
                )}
            </div>
        )}

        {viewState === 'result' && apiResult && (
            <div className="absolute inset-0 z-10 pt-[80px] pb-10 px-8 md:px-16 overflow-y-auto scroll-smooth" ref={resultRef}>
                <div className="max-w-4xl mx-auto fade-in">
                    <div className="mb-10 border-b border-gray-800 pb-6">
                        <h1 className="text-4xl font-bold text-white mb-4">Prezado <span className="text-[#1DB954]">{apiResult.nome}</span>,</h1>
                        <p className="text-lg text-gray-300 leading-relaxed text-justify">{apiResult.resumo_analise}</p>
                    </div>
                    
                    {apiResult.sugestao && (
                        <div className="space-y-10">
                            {Object.entries(apiResult.sugestao).map(([portfolioName, items], index) => (
                                <div key={index} className="bg-[#2a2a2a] bg-opacity-40 p-6 rounded-lg border-l-4 border-[#1DB954] hover:bg-opacity-60 transition-all">
                                    <h3 className="text-2xl font-bold text-[#1ED760] mb-4">{portfolioName}</h3>
                                    <ul className="space-y-4">
                                        {typeof items === 'object' && items !== null ? (
                                            Object.entries(items).map(([key, description]) => (
                                                <li key={key} className="flex items-start gap-3">
                                                    <span className="mt-1.5 min-w-[8px] min-h-[8px] rounded-full bg-white"></span>
                                                    <span className="text-gray-200 text-base font-light leading-relaxed">{description}</span>
                                                </li>
                                            ))
                                        ) : (
                                            <li className="text-gray-200">{JSON.stringify(items)}</li>
                                        )}
                                    </ul>
                                </div>
                            ))}
                        </div>
                    )}

                    <div className="mt-16 text-center text-xs text-gray-600 uppercase tracking-widest">
                        <p>InvestWise • IA Financeira</p>
                    </div>
                </div>
            </div>
        )}

      </div>
    </div>
  );
};

export default InvestWiseApp;