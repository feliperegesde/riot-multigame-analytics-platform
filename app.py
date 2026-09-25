import streamlit as st
from src.lol.api_client import LolAPIClient
from src.lol.processor import LolMatchProcessor
from src.valorant.api_client import ValorantAPIClient
from src.valorant.processor import ValorantMatchProcessor
from src.shared.cluster_model import PlaystyleClusterer

st.set_page_config(page_title="Riot Multi-Game Scouting Platform", layout="wide")

st.title("🎮 Riot Games Multi-Game Analytics Platform")
st.markdown("Plataforma avançada de scouting e análise comportamental para League of Legends e Valorant.")

# Seletor de Jogo
st.sidebar.header("Configurações do Sistema")
game_choice = st.sidebar.selectbox("Selecione o Jogo", ["League of Legends", "Valorant"])

if game_choice == "League of Legends":
    st.sidebar.subheader("Credenciais LoL")
    api_key = st.sidebar.text_input("Riot API Key", type="password")
    game_name = st.sidebar.text_input("Game Name", value="Future")
    tag_line = st.sidebar.text_input("Tag Line", value="BR1")
    match_count = st.sidebar.slider("Quantidade de Partidas", 5, 20, 10)

    if st.sidebar.button("Analisar Partidas de LoL"):
        if not api_key:
            st.error("Insira uma chave válida da Riot API.")
        else:
            try:
                client = LolAPIClient(api_key)
                with st.spinner("Minerando dados detalhados do League of Legends..."):
                    puuid = client.get_puuid_by_riot_id(game_name, tag_line)
                    match_ids = client.get_match_ids(puuid, count=match_count)
                    
                    stats = [LolMatchProcessor.extract_player_stats(client.get_match_details(m), puuid) for m in match_ids]
                    valid_stats = [s for s in stats if s is not None]
                    
                    if not valid_stats:
                        st.warning("Não foi possível encontrar dados válidos para as partidas recentes deste invocador.")
                    else:
                        df = LolMatchProcessor.create_dataframe(valid_stats)
                        
                        clusterer = PlaystyleClusterer()
                        df = clusterer.fit_predict(df, ["kda", "cs_per_min", "damage_share_pct", "vision_score"])

                        st.success("Análise de LoL concluída com sucesso!")
                        
                        # Métricas Principais (KPIs)
                        col1, col2, col3, col4, col5 = st.columns(5)
                        col1.metric("Partidas Analisadas", len(df))
                        col2.metric("Taxa de Vitória", f"{(df['win'].mean() * 100):.1f}%")
                        col3.metric("KDA Médio", f"{df['kda'].mean():.2f}")
                        col4.metric("Dano Médio ao Time", f"{df['damage_share_pct'].mean():.1f}%")
                        col5.metric("CS / Min Médio", f"{df['cs_per_min'].mean():.1f}")

                        # SISTEMA DE ABAS PARA EXPLORAÇÃO PROFUNDA
                        tab1, tab2, tab3, tab4, tab5 = st.tabs([
                            "📊 Histórico & Tabela", 
                            "🎯 Impacto & Dano", 
                            "💰 Economia & Ouro", 
                            "🌾 Farm & Desempenho", 
                            "👁️ Visão & Mapa"
                        ])

                        with tab1:
                            st.subheader("Histórico Detalhado por Partida")
                            st.dataframe(df[[
                                "champion_name", "individual_position", "win", "kills", 
                                "deaths", "assists", "kda", "cs_per_min", "playstyle_label"
                            ]], use_container_width=True)

                        with tab2:
                            st.subheader("Participação de Dano (%) por Partida")
                            st.markdown("Avalia o quanto da agressividade e do dano total da equipe passou pelas suas mãos.")
                            st.bar_chart(df["damage_share_pct"])

                        with tab3:
                            st.subheader("Evolução de Ouro Ganho (Gold Earned)")
                            st.markdown("Acompanhe o crescimento econômico acumulado ao longo das partidas.")
                            st.line_chart(df["gold_earned"])

                        with tab4:
                            st.subheader("Eficiência de Farm (CS por Minuto)")
                            st.markdown("Mede a constância na coleta de recursos e tropas por minuto de jogo.")
                            st.line_chart(df["cs_per_min"])

                        with tab5:
                            st.subheader("Controle de Visão e Wards")
                            st.markdown("Monitora a sua pontuação de visão combinada com wards destruídas.")
                            st.line_chart(df[["vision_score", "wards_killed"]])

            except Exception as e:
                st.error(f"Ocorreu um erro: {e}")

elif game_choice == "Valorant":
    st.sidebar.subheader("Credenciais Valorant")
    region = st.sidebar.selectbox("Região", ["br", "na", "eu", "ap"])
    val_name = st.sidebar.text_input("Riot Name", value="Future")
    val_tag = st.sidebar.text_input("Tag", value="BR1")
    val_size = st.sidebar.slider("Quantidade de Partidas", 5, 20, 10)

    if st.sidebar.button("Analisar Partidas de Valorant"):
        try:
            client = ValorantAPIClient()
            with st.spinner("Minerando dados do Valorant..."):
                matches = client.get_match_history(region, val_name, val_tag, size=val_size)
                
                stats = [ValorantMatchProcessor.extract_player_stats(m, val_name) for m in matches]
                valid_stats = [s for s in stats if s is not None]

                if not valid_stats:
                    st.warning("Não foram encontradas partidas válidas para este perfil de Valorant.")
                else:
                    df = ValorantMatchProcessor.create_dataframe(valid_stats)
                    
                    clusterer = PlaystyleClusterer()
                    df = clusterer.fit_predict(df, ["kda", "acs", "damage_made"])

                    st.success("Análise de Valorant concluída com sucesso!")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Partidas", len(df))
                    col2.metric("ACS Médio", f"{df['acs'].mean():.1f}")
                    col3.metric("KDA Médio", f"{df['kda'].mean():.2f}")
                    col4.metric("Dano Total Médio", f"{df['damage_made'].mean():.1f}")

                    st.subheader("📊 Histórico de Agentes e Mapas")
                    st.dataframe(df[["map", "agent", "team", "kills", "deaths", "assists", "kda", "acs", "playstyle_label"]], use_container_width=True)

                    st.subheader("🎯 Evolução do Combat Score (ACS)")
                    st.line_chart(df["acs"])
        except Exception as e:
            st.error(f"Ocorreu um erro: {e}")