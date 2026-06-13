# Projeto Final — Dashboard Spotify com Python e Dash

## Tema
Análise de tendências musicais no Spotify: popularidade, gêneros e atributos musicais.

## Objetivo
Construir um dashboard interativo para analisar como características musicais, como energia, danceability, valence, acousticness, tempo e gênero, se relacionam com a popularidade das faixas.

## Dataset sugerido
Use o dataset do Kaggle: **114000 Spotify Songs** ou **Spotify Tracks Dataset**.

O arquivo principal normalmente vem como `dataset.csv`.  
Para cumprir o requisito de pelo menos dois arquivos, o projeto possui um script que divide o dataset em dois arquivos distintos:

- `tracks_metadata.csv`
- `tracks_audio_features.csv`

Depois, o pipeline realiza `merge` entre eles usando `track_id`.

## Estrutura do projeto

```text
projeto_spotify_dash/
│
├── app.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── raw/
│   │   └── coloque_aqui_o_dataset.csv
│   └── processed/
│
├── src/
│   ├── prepare_data.py
│   └── eda_insights.py
│
└── assets/
    └── style.css
```

## Como rodar

1. Instale as bibliotecas:

```bash
pip install -r requirements.txt
```

2. Baixe o dataset do Kaggle e coloque o CSV em:

```text
data/raw/dataset.csv
```

3. Prepare os dados:

```bash
python src/prepare_data.py
```

4. Rode o dashboard:

```bash
python app.py
```

5. Acesse no navegador:

```text
http://127.0.0.1:8050
```

## Entregáveis

- Código do projeto
- Dataset bruto usado
- Dashboard com duas abas:
  - Visão Geral
  - Exploração Interativa
- Relatório/apresentação explicando:
  - fonte dos dados
  - pipeline
  - limpeza
  - transformações
  - insights
