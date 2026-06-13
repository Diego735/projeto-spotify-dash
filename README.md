desenvolvemos um pipeline de captura automática de dados integrado diretamente com a **Web API oficial do Spotify** utilizando a biblioteca `spotipy`.

### Arquitetura do Pipeline de Dados
1. **Coleta (`src/coleta_spotify.py`):** O script realiza uma autenticação segura via *Client Credentials* no painel de desenvolvedor do Spotify e consome o endpoint de busca (`sp.search`). Ele coleta em tempo real as músicas e artistas que estão em alta em 6 gêneros musicais estratégicos (*pop, rock, hip-hop, electronic, jazz, brazil*), exportando os dados brutos para `data/raw/dataset.csv`.
2. **Processamento (`src/prepare_data.py`):** Consome o arquivo bruto gerado pelo crawler, executa os tratamentos de dados, limpeza, engenharia de recursos (como a definição de perfis musicais e a regra de classificação de `is_hit`) e gera a base final limpa em `data/processed/spotify_clean.csv`.
3. **Visualização (`app.py`):** O dashboard lê a base de dados atualizada pelo crawler e renderiza os gráficos interativos de tendências.

### Como rodar o fluxo completo de atualização:
```bash
# 1. Executar o crawler para buscar dados novos na API do Spotify
python projeto_spotify_dash/src/coleta_spotify.py

# 2. Executar o script de tratamento e preparação dos dados
python projeto_spotify_dash/src/prepare_data.py

# 3. Iniciar o servidor do Dashboard
python projeto_spotify_dash/app.py

--------------------------------------------------------------------------------------------------------------------------------------------------------------

Este é um banco de dados histórico massivo hospedado no Kaggle contendo mais de 232.000 músicas.
Ele organiza as músicas por colunas como genre (gênero), artist_name, track_name, popularity e os atributos de áudio (como danceability, energy, tempo).
Serve como a excelente base de dados de treino e referência histórica. Ele ajuda a entender como os gêneros musicais se comportavam estruturalmente antes de você começar a puxar os dados mais recentes direto da API.

https://www.kaggle.com/datasets/zaheenhamidani/ultimate-spotify-tracks-db?utm_source=chatgpt.com


Este é outro dataset extremamente popular no Kaggle, focado em 114.000 faixas de música individualizadas com um nível de detalhe técnico muito alto.
A diferença crucial deste dataset é que ele foi extraído com foco em áudio quantitativo puro, trazendo métricas exatas de acousticness, danceability, loudness, speechiness e a coluna explicit (se a música tem conteúdo explícito ou não).
Este link representa a estrutura exata de colunas e dados que o seu script prepare_data.py e o seu Dashboard original esperam ler. É o "molde" ideal que dita o formato que o seu arquivo final tratados deve ter.

https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset?resource=download



Este link é o coração do seu crawler. Ele aponta direto para a central de controle do aplicativo privado que você criou dentro da plataforma oficial do Spotify para Desenvolvedores.
É aqui que ficam armazenadas as suas chaves de segurança exclusivas: o Client ID e o Client Secret.
Sem esse link e as credenciais que estão dentro dele, o script coleta_spotify.py não conseguiria pedir autorização aos servidores do Spotify. Ele funciona como o "crachá de acesso" que permite ao seu código Python contornar as restrições locais, fazer buscas em tempo real por gênero e trazer as músicas mais tocadas de 2026 para dentro do seu sistema automaticamente.

https://developer.spotify.com/dashboard/9680df6280054ddebc700c2e1d75fb35


>>>>>>>Usamos os dois primeiros links do Kaggle como nossa base de dados estática de referência histórica para modelar e estruturar nossos gráficos. O terceiro link é o nosso Painel do Spotify API, de onde extraímos as credenciais para rodar o crawler dinâmico que atualiza o projeto com dados reais



Projeto Final — Dashboard Spotify com Python e Dash
Tema
Análise de tendências musicais no Spotify: popularidade, gêneros e atributos musicais.

Objetivo
Construir um dashboard interativo para analisar como características musicais, como energia, danceability, valence, acousticness, tempo e gênero, se relacionam com a popularidade das faixas.

Dataset sugerido
Use o dataset do Kaggle: 114000 Spotify Songs ou Spotify Tracks Dataset.

O arquivo principal normalmente vem como dataset.csv.
Para cumprir o requisito de pelo menos dois arquivos, o projeto possui um script que divide o dataset em dois arquivos distintos:

tracks_metadata.csv
tracks_audio_features.csv
Depois, o pipeline realiza merge entre eles usando track_id.

Estrutura do projeto
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
Como rodar
Instale as bibliotecas:
pip install -r requirements.txt
Baixe o dataset do Kaggle e coloque o CSV em:
data/raw/dataset.csv
Prepare os dados:
python src/prepare_data.py
Rode o dashboard:
python app.py
Acesse no navegador:
http://127.0.0.1:8050
Entregáveis
Código do projeto
Dataset bruto usado
Dashboard com duas abas:
Visão Geral
Exploração Interativa
Relatório/apresentação explicando:
fonte dos dados
pipeline
limpeza
transformações
insights
