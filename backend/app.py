import streamlit as st
from backend.src.api_client import LolAPIClient
from backend.src.processor import MatchProcessor
from backend.src.cluster_model import PlaystyleClusterer

st.set_page_config(
    page_title="LoL Advanced Analytics & Scouting",
    page_icon="🎮",
    layout="wide"
)

# Estilização visual limpa
st.markdown("""
    <style>
        .main-title { font-size: 2.5rem; font-weight: 700; color: #FF4B4B; margin-bottom: 0px; }
        .sub-title { font-size: 1.1rem; color: #6c757d; margin-bottom: 2rem; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">LoL Advanced Scouting & Performance Platform</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Plataforma analítica profissional para diagnóstico de desempenho, economia e comportamento em partidas.</p>', unsafe_allow_html=True)

@st.cache_data(ttl=3600)
def fetch_player_data(api_key: str, game_name: str, tag_line: str, match_count: int) -> list[dict]:
    client = LolAPIClient(api_key)
    puuid = client.get_puuid_by_riot_id(game_name, tag_line)
    match_ids = client.get_match_ids(puuid, count=match_count)
    
    stats_list = []
    for m_id in match_ids:
        match_details = client.get_match_details(m_id)
        parsed_stats = MatchProcessor.extract_player_stats(match_details, puuid)
        if parsed_stats:
            stats_list.append(parsed_stats)
            
    return stats_list

# Sidebar de Configuração
st.sidebar.header("⚙️ Configurações de Consulta")
api_key = st.sidebar.text_input("Riot API Key", type="password", help="Insira sua chave de desenvolvedor da Riot.")
game_name = st.sidebar.text_input("Game Name", value="Future")
tag_line = st.sidebar.text_input("Tag Line", value="BR1")
match_count = st.sidebar.slider("Quantidade de Partidas", min_value=5, max_value=20, value=10)

if st.sidebar.button("Executar Análise Profunda", type="primary"):
    if not api_key:
        st.error("Por favor, insira uma chave da Riot API válida.")
    else:
        try:
            with st.spinner("Minerando dados e calculando métricas avançadas..."):
                stats_list = fetch_player_data(api_key, game_name, tag_line, match_count)
                
                if not stats_list:
                    st.warning("Nenhuma partida encontrada para este invocador.")
                else:
                    df_stats = MatchProcessor.create_dataframe_from_stats(stats_list)
                    
                    clusterer = PlaystyleClusterer(n_clusters=2)
                    df_clustered = clusterer.fit_predict(df_stats, ["kda", "cs_per_min", "damage_share_pct", "vision_score"])

                    st.success("Análise minerada com sucesso!")

                    # KPIs Executivos no topo
                    col1, col2, col3, col4, col5 = st.columns(5)
                    col1.metric("Partidas Analisadas", len(df_clustered))
                    col2.metric("Taxa de Vitória", f"{(df_clustered['win'].mean() * 100):.1f}%")
                    col3.metric("KDA Médio", f"{df_clustered['kda'].mean():.2f}")
                    col4.metric("Dano Médio ao Time", f"{df_clustered['damage_share_pct'].mean():.1f}%")
                    col5.metric("CS / Min Médio", f"{df_clustered['cs_per_min'].mean():.1f}")

                    st.markdown("---")

                    # Organização em Abas Profissionais
                    tab1, tab2, tab3, tab4, tab5 = st.tabs([
                        "📊 Histórico & Campeões", 
                        "🎯 Participação de Dano", 
                        "💰 Crescimento Econômico (Ouro)", 
                        "🌾 Eficiência de Farm (CS/min)", 
                        "👁️ Controle de Visão"
                    ])

                    with tab1:
                        st.subheader("Histórico Detalhado e Classificação de Estilo")
                        st.markdown("Tabela completa contendo os campeões jogados, posições, KDA e o cluster comportamental gerado por Machine Learning.")
                        st.dataframe(df_clustered[[
                            "champion_name", "individual_position", "win", "kills", 
                            "deaths", "assists", "kda", "cs_per_min", "playstyle_label"
                        ]], use_container_width=True)

                    with tab2:
                        st.subheader("Análise de Dano Causado ao Time (%)")
                        st.markdown("Mostra o impacto ofensivo real em comparação com os demais aliados na partida.")
                        st.bar_chart(df_clustered["damage_share_pct"])

                    with tab3:
                        st.subheader("Evolução de Ouro Acumulado por Partida")
                        st.markdown("Acompanhe o rendimento financeiro bruto obtido ao longo das disputas recentes.")
                        st.line_chart(df_clustered["gold_earned"])

                    with tab4:
                        st.subheader("Consistência de Farm (CS por Minuto)")
                        st.markdown("Mede a disciplina de coleta de recursos e tropas por minuto de jogo.")
                        st.line_chart(df_clustered["cs_per_min"])

                    with tab5:
                        st.subheader("Pontuação de Visão vs Wards Destruídas")
                        st.markdown("Avalia o trabalho de visão de mapa, limpeza de sentinelas e controle de objetivos.")
                        st.line_chart(df_clustered[["vision_score", "wards_killed"]])

        except Exception as e:
            st.error(f"Ocorreu um erro ao processar os dados: {e}")