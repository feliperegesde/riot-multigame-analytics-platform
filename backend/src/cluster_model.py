import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

class PlaystyleClusterer:
    def __init__(self, n_clusters: int = 2):
        self.n_clusters = n_clusters
        self.scaler = StandardScaler()
        self.model = KMeans(n_clusters=self.n_clusters, random_state=42, n_init=10)

    def fit_predict(self, df: pd.DataFrame, features: list[str]) -> pd.DataFrame:
        if df.empty or len(df) < self.n_clusters:
            df["cluster"] = 0
            return df

        X = df[features].fillna(0)
        X_scaled = self.scaler.fit_transform(X)
        
        df["cluster"] = self.model.fit_predict(X_scaled)
        cluster_labels = {0: "Estilo Estratégico / Objetivo", 1: "Estilo Agressivo / Combatente"}
        df["playstyle_label"] = df["cluster"].map(cluster_labels).fillna("Estilo Misto")
        
        return df