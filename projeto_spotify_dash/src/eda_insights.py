from pathlib import Path
import pandas as pd

DATA_FILE = Path("data/processed/spotify_clean.csv")

def main():
    if not DATA_FILE.exists():
        raise FileNotFoundError("Rode primeiro: python src/prepare_data.py")

    df = pd.read_csv(DATA_FILE)

    print("\n===== RESUMO GERAL =====")
    print(f"Total de músicas: {len(df):,}")
    print(f"Total de artistas: {df['main_artist'].nunique():,}")
    print(f"Total de gêneros: {df['genre'].nunique():,}")
    print(f"Popularidade média: {df['popularity'].mean():.2f}")

    print("\n===== TOP 10 GÊNEROS POR POPULARIDADE MÉDIA =====")
    print(
        df.groupby("genre")["popularity"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
    )

    print("\n===== TOP 10 ARTISTAS COM MAIS HITS =====")
    print(
        df[df["is_hit"] == "Hit"]
        .groupby("main_artist")["track_id"]
        .count()
        .sort_values(ascending=False)
        .head(10)
    )

    print("\n===== CORRELAÇÕES COM POPULARIDADE =====")
    features = ["danceability", "energy", "valence", "acousticness", "speechiness", "tempo", "duration_min"]
    print(df[features + ["popularity"]].corr(numeric_only=True)["popularity"].sort_values(ascending=False))

    print("\n===== INSIGHTS SUGERIDOS =====")
    print("1. Compare os gêneros com maior popularidade média e o volume de músicas.")
    print("2. Analise se músicas mais dançantes possuem maior popularidade.")
    print("3. Verifique se músicas mais acústicas têm comportamento diferente.")
    print("4. Compare artistas com mais hits e gêneros dominantes.")
    print("5. Observe quais perfis musicais concentram músicas mais populares.")

if __name__ == "__main__":
    main()
