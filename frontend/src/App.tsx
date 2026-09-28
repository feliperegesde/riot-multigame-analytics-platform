import React, { useState } from 'react';
import axios from 'axios';

interface Match {
  champion_name: string;
  individual_position: string;
  win: number;
  kills: number;
  deaths: number;
  assists: number;
  kda: number;
  cs_per_min: number;
  playstyle_label: string;
}

interface AnalysisData {
  summoner: string;
  total_matches: number;
  winrate: number;
  avg_kda: number;
  avg_damage_share: number;
  avg_cs_min: number;
  matches: Match[];
}

export default function App() {
  const [gameName, setGameName] = useState('future');
  const [tagLine, setTagLine] = useState('jare');
  const [apiKey, setApiKey] = useState('');
  const [matchCount, setMatchCount] = useState(10);
  const [activeTab, setActiveTab] = useState('history');
  const [data, setData] = useState<AnalysisData | null>(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await axios.post('/api/analyze', {
        api_key: apiKey,
        game_name: gameName,
        tag_line: tagLine,
        match_count: matchCount
      });
      setData(response.data);
    } catch (err: any) {
      console.error("Erro detalhado do Axios:", err);
      alert(`Erro na busca: ${err.response?.data?.detail || err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0b0e14] text-gray-200 flex font-sans">
      {/* SIDEBAR DE CONFIGURAÇÕES */}
      <aside className="w-80 bg-[#12161f] border-r border-gray-800 p-6 flex flex-col justify-between">
        <div>
          <div className="flex items-center space-x-2 mb-8">
            <span className="bg-[#FF0055] text-white text-xs font-bold px-2 py-1 rounded">LoL</span>
            <h1 className="text-lg font-black tracking-wider text-white">ADVANCED <span className="text-gray-400 font-light text-xs block">ANALYTICS</span></h1>
          </div>

          <form onSubmit={handleAnalyze} className="space-y-5">
            <div>
              <label className="text-xs uppercase tracking-wider text-gray-400 font-semibold block mb-1">Riot API Key</label>
              <input 
                type="password" 
                value={apiKey} 
                onChange={(e) => setApiKey(e.target.value)}
                placeholder="RGAPI-..."
                className="w-full bg-[#181d28] border border-gray-700 rounded p-2 text-sm text-white focus:border-[#FF0055] outline-none"
              />
            </div>

            <div>
              <label className="text-xs uppercase tracking-wider text-gray-400 font-semibold block mb-1">Game Name</label>
              <input 
                type="text" 
                value={gameName} 
                onChange={(e) => setGameName(e.target.value)}
                className="w-full bg-[#181d28] border border-gray-700 rounded p-2 text-sm text-white focus:border-[#FF0055] outline-none"
              />
            </div>

            <div>
              <label className="text-xs uppercase tracking-wider text-gray-400 font-semibold block mb-1">Tag Line</label>
              <input 
                type="text" 
                value={tagLine} 
                onChange={(e) => setTagLine(e.target.value)}
                className="w-full bg-[#181d28] border border-gray-700 rounded p-2 text-sm text-white focus:border-[#FF0055] outline-none"
              />
            </div>

            <div>
              <div className="flex justify-between text-xs text-gray-400 mb-1">
                <span>Partidas</span>
                <span className="text-[#FF0055] font-bold">{matchCount}</span>
              </div>
              <input 
                type="range" 
                min="1" 
                max="50" 
                value={matchCount} 
                onChange={(e) => setMatchCount(Number(e.target.value))}
                className="w-full accent-[#FF0055] cursor-pointer"
              />
            </div>

            <button 
              type="submit" 
              disabled={loading}
              className="w-full bg-[#FF0055] hover:bg-[#e0004b] text-white font-bold py-3 rounded text-sm tracking-wider uppercase transition shadow-lg shadow-[#FF0055]/20 cursor-pointer"
            >
              {loading ? 'Minerando...' : 'Executar Análise'}
            </button>
          </form>
        </div>

        <div className="text-xs text-gray-500 border-t border-gray-800 pt-4">
          Status: <span className="text-green-500 font-semibold">● Sistema Online</span>
        </div>
      </aside>

      {/* PAINEL PRINCIPAL */}
      <main className="flex-1 p-8 overflow-y-auto">
        {/* HEADER DE PERFIL */}
        <header className="flex justify-between items-center mb-8 bg-[#12161f] border border-gray-800 p-6 rounded-lg">
          <div>
            <h2 className="text-2xl font-black text-white tracking-wide">
              {gameName}<span className="text-[#FF0055]">#{tagLine}</span>
            </h2>
            <p className="text-xs text-gray-400 uppercase tracking-widest mt-1">Perfil de Análise • Ativo</p>
          </div>
          <div className="flex items-center space-x-2 bg-green-500/10 border border-green-500/30 px-3 py-1.5 rounded-full text-green-400 text-xs font-semibold">
            <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
            <span>Sistema Online</span>
          </div>
        </header>

        {/* CARDS DE MÉTRICAS */}
        <div className="grid grid-cols-5 gap-4 mb-8">
          <div className="bg-[#12161f] border border-gray-800 p-4 rounded-lg">
            <span className="text-[10px] uppercase text-gray-400 font-bold tracking-wider">Partidas Analisadas</span>
            <div className="text-2xl font-black text-white mt-1">{data ? data.total_matches : '—'}</div>
            <span className="text-[10px] text-gray-500">total</span>
          </div>
          <div className="bg-[#12161f] border border-gray-800 p-4 rounded-lg">
            <span className="text-[10px] uppercase text-gray-400 font-bold tracking-wider">Taxa de Vitória</span>
            <div className="text-2xl font-black text-white mt-1">{data ? `${data.winrate}%` : '—'}</div>
            <span className="text-[10px] text-gray-500">geral</span>
          </div>
          <div className="bg-[#12161f] border border-gray-800 p-4 rounded-lg">
            <span className="text-[10px] uppercase text-gray-400 font-bold tracking-wider">KDA Médio</span>
            <div className="text-2xl font-black text-white mt-1">{data ? data.avg_kda : '—'}</div>
            <span className="text-[10px] text-gray-500">kills+assists/deaths</span>
          </div>
          <div className="bg-[#12161f] border border-gray-800 p-4 rounded-lg">
            <span className="text-[10px] uppercase text-gray-400 font-bold tracking-wider">Dano Médio ao Time</span>
            <div className="text-2xl font-black text-white mt-1">{data ? `${data.avg_damage_share}%` : '—'}</div>
            <span className="text-[10px] text-gray-500">participação</span>
          </div>
          <div className="bg-[#12161f] border border-gray-800 p-4 rounded-lg">
            <span className="text-[10px] uppercase text-gray-400 font-bold tracking-wider">CS / Min Médio</span>
            <div className="text-2xl font-black text-white mt-1">{data ? data.avg_cs_min : '—'}</div>
            <span className="text-[10px] text-gray-500">média geral</span>
          </div>
        </div>

        {/* ABAS DE NAVEGAÇÃO */}
        <div className="flex border-b border-gray-800 mb-6 space-x-8 text-sm font-semibold">
          <button 
            onClick={() => setActiveTab('history')}
            className={`pb-3 border-b-2 transition cursor-pointer ${activeTab === 'history' ? 'border-[#FF0055] text-white' : 'border-transparent text-gray-400 hover:text-gray-200'}`}
          >
            ⚔️ HISTÓRICO & CAMPEÕES
          </button>
          <button 
            onClick={() => setActiveTab('damage')}
            className={`pb-3 border-b-2 transition cursor-pointer ${activeTab === 'damage' ? 'border-[#FF0055] text-white' : 'border-transparent text-gray-400 hover:text-gray-200'}`}
          >
            🎯 PARTICIPAÇÃO DE DANO
          </button>
          <button 
            onClick={() => setActiveTab('economy')}
            className={`pb-3 border-b-2 transition cursor-pointer ${activeTab === 'economy' ? 'border-[#FF0055] text-white' : 'border-transparent text-gray-400 hover:text-gray-200'}`}
          >
            📈 CRESCIMENTO ECONÔMICO
          </button>
        </div>

        {/* CONTEÚDO DAS ABAS */}
        <div className="bg-[#12161f] border border-gray-800 rounded-lg p-6">
          {activeTab === 'history' && (
            <div>
              <h3 className="text-lg font-bold text-white mb-1">HISTÓRICO DETALHADO</h3>
              <p className="text-xs text-gray-400 mb-6">Campeões jogados, posições, KDA e classificação comportamental via Machine Learning.</p>
              
              <div className="overflow-x-auto">
                <table className="w-full text-left border-collapse">
                  <thead>
                    <tr className="border-b border-gray-800 text-xs text-gray-400 uppercase tracking-wider">
                      <th className="pb-3">Campeão</th>
                      <th className="pb-3">Posição</th>
                      <th className="pb-3">Resultado</th>
                      <th className="pb-3">K / D / A</th>
                      <th className="pb-3">KDA</th>
                      <th className="pb-3">CS/Min</th>
                      <th className="pb-3">Estilo (ML)</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-800/50 text-sm">
                    {data && data.matches.length > 0 ? (
                      data.matches.map((m, idx) => (
                        <tr key={idx} className="hover:bg-gray-800/20 transition">
                          <td className="py-3 font-bold text-white">{m.champion_name}</td>
                          <td className="py-3 text-xs font-semibold text-gray-400">{m.individual_position}</td>
                          <td className="py-3">
                            <span className={`px-2 py-1 rounded text-xs font-bold ${m.win === 1 ? 'bg-green-500/10 text-green-400 border border-green-500/30' : 'bg-red-500/10 text-red-400 border border-red-500/30'}`}>
                              {m.win === 1 ? 'VITÓRIA' : 'DERROTA'}
                            </span>
                          </td>
                          <td className="py-3 font-mono">{m.kills} / {m.deaths} / {m.assists}</td>
                          <td className="py-3 font-mono font-bold text-[#FF0055]">{m.kda}</td>
                          <td className="py-3 font-mono">{m.cs_per_min}</td>
                          <td className="py-3 text-xs text-gray-300">{m.playstyle_label}</td>
                        </tr>
                      ))
                    ) : (
                      <tr>
                        <td colSpan={7} className="py-8 text-center text-gray-500">Nenhum dado carregado. Insira suas credenciais e clique em Executar Análise.</td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {activeTab === 'damage' && (
            <div>
              <h3 className="text-lg font-bold text-white mb-1">PARTICIPAÇÃO DE DANO</h3>
              <p className="text-xs text-gray-400 mb-6">Distribuição de dano causado por campeão ao longo das partidas analisadas.</p>
              <div className="h-64 flex items-center justify-center border border-dashed border-gray-800 rounded text-gray-500 text-sm">
                Gráficos de distribuição de dano prontos para integração com Recharts / Chart.js
              </div>
            </div>
          )}

          {activeTab === 'economy' && (
            <div>
              <h3 className="text-lg font-bold text-white mb-1">CRESCIMENTO ECONÔMICO</h3>
              <p className="text-xs text-gray-400 mb-6">Evolução de ouro ao longo do tempo vs média da plataforma.</p>
              <div className="h-64 flex items-center justify-center border border-dashed border-gray-800 rounded text-gray-500 text-sm">
                Gráfico de linha comparativa de ouro pronto para integração com Recharts
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}