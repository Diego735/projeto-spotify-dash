from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

INPUT_FILE = RAW_DIR / "dataset.csv"

def find_column(df, options):
    lower_map = {c.lower(): c for c in df.columns}
    for opt in options:
        if opt.lower() in lower_map:
            return lower_map[opt.lower()]
    return None

def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            "Coloque o arquivo dataset.csv em data/raw/. "
            "Exemplo: data/raw/dataset.csv"
        )

    df = pd.read_csv(INPUT_FILE)

    # Padronização dos nomes das colunas
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    # Tenta identificar colunas comuns em datasets Spotify
    track_id_col = find_column(df, ["track_id", "id"])
    track_name_col = find_column(df, ["track_name", "name", "track"])
    artist_col = find_column(df, ["artists", "artist_name", "artist"])
    genre_col = find_column(df, ["track_genre", "genre"])
    popularity_col = find_column(df, ["popularity"])

    if track_id_col is None:
        df["track_id"] = range(1, len(df) + 1)
        track_id_col = "track_id"

    rename_map = {
        track_id_col: "track_id",
    }

    if track_name_col:
        rename_map[track_name_col] = "track_name"
    if artist_col:
        rename_map[artist_col] = "artists"
    if genre_col:
        rename_map[genre_col] = "genre"
    if popularity_col:
        rename_map[popularity_col] = "popularity"

    df = df.rename(columns=rename_map)

    required_defaults = {
        "track_name": "Desconhecido",
        "artists": "Desconhecido",
        "genre": "Não informado",
        "popularity": 0,
        "danceability": np.nan,
        "energy": np.nan,
        "valence": np.nan,
        "acousticness": np.nan,
        "speechiness": np.nan,
        "instrumentalness": np.nan,
        "liveness": np.nan,
        "tempo": np.nan,
        "duration_ms": np.nan,
        "explicit": False,
    }

    for col, default in required_defaults.items():
        if col not in df.columns:
            df[col] = default

    # Remove duplicados
    df = df.drop_duplicates(subset=["track_id"])

    # Tratamento de valores ausentes
    categorical_cols = ["track_name", "artists", "genre"]
    for col in categorical_cols:
        df[col] = df[col].fillna("Não informado").astype(str).str.strip()

    numeric_cols = [
        "popularity", "danceability", "energy", "valence",
        "acousticness", "speechiness", "instrumentalness",
        "liveness", "tempo", "duration_ms"
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        df[col] = df[col].fillna(df[col].median())

    # Padronização de formatos
    df["genre"] = df["genre"].str.title()
    df["artists"] = df["artists"].str.replace(";", ",", regex=False)
    df["main_artist"] = df["artists"].str.split(",").str[0].str.strip().str.title()

    # Criação de novas variáveis
    df["duration_min"] = df["duration_ms"] / 60000

    df["popularity_level"] = pd.cut(
        df["popularity"],
        bins=[-1, 39, 69, 100],
        labels=["Baixa", "Média", "Alta"]
    )

    df["is_hit"] = np.where(df["popularity"] >= 70, "Hit", "Não hit")

    df["music_profile"] = np.select(
        [
            (df["energy"] >= 0.7) & (df["danceability"] >= 0.7),
            (df["acousticness"] >= 0.6),
            (df["valence"] >= 0.7),
            (df["speechiness"] >= 0.3),
        ],
        [
            "Dançante e energética",
            "Acústica",
            "Positiva",
            "Falado/Rap"
        ],
        default="Equilibrada"
    )

    # Normalização para radar
    scaler = MinMaxScaler()
    scale_cols = ["danceability", "energy", "valence", "acousticness", "speechiness"]
    df[[f"{c}_scaled" for c in scale_cols]] = scaler.fit_transform(df[scale_cols])

    # Cria dois arquivos distintos para demonstrar integração com merge
    metadata_cols = [
        "track_id", "track_name", "artists", "main_artist",
        "genre", "popularity", "popularity_level", "is_hit", "explicit"
    ]

    features_cols = [
        "track_id", "danceability", "energy", "valence",
        "acousticness", "speechiness", "instrumentalness",
        "liveness", "tempo", "duration_ms", "duration_min",
        "music_profile"
    ]

    tracks_metadata = df[metadata_cols].copy()
    tracks_audio_features = df[features_cols].copy()

    tracks_metadata.to_csv(RAW_DIR / "tracks_metadata.csv", index=False)
    tracks_audio_features.to_csv(RAW_DIR / "tracks_audio_features.csv", index=False)

    # Integração por merge
    final_df = tracks_metadata.merge(tracks_audio_features, on="track_id", how="inner")

    final_df.to_csv(PROCESSED_DIR / "spotify_clean.csv", index=False)

    print("Pipeline concluído com sucesso.")
    print(f"Registros finais: {len(final_df):,}")
    print("Arquivo gerado: data/processed/spotify_clean.csv")
    print("Arquivos distintos gerados para integração:")
    print("- data/raw/tracks_metadata.csv")
    print("- data/raw/tracks_audio_features.csv")

if __name__ == "__main__":
    main()
