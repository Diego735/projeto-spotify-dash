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
