# Relatório / Roteiro de Apresentação

## 1. Título
**Análise de Tendências Musicais no Spotify**

## 2. Objetivo do projeto
O objetivo do projeto é analisar músicas disponíveis em uma base pública do Spotify para identificar padrões relacionados à popularidade das faixas, considerando atributos musicais como energia, danceability, valence, acousticness, tempo, gênero e artista.

## 3. Fonte dos dados
A base utilizada foi obtida no Kaggle, em datasets públicos de músicas do Spotify. A base contém mais de 10.000 registros e informações sobre faixas musicais, artistas, gêneros e atributos sonoros.

## 4. Aquisição dos dados
Os dados foram carregados em Python utilizando a biblioteca Pandas. O arquivo original foi colocado na pasta `data/raw` e processado pelo script `prepare_data.py`.

## 5. Integração dos dados
Para atender ao requisito de integração, o dataset foi separado em dois arquivos distintos:

- `tracks_metadata.csv`: informações de identificação da música, artista, gênero e popularidade.
- `tracks_audio_features.csv`: atributos musicais como energia, danceability, valence, acousticness e tempo.

Após isso, os arquivos foram integrados novamente por meio de um `merge` utilizando a coluna `track_id`.

## 6. Limpeza e tratamento
Foram realizadas as seguintes etapas:

- remoção de registros duplicados;
- tratamento de valores ausentes;
- conversão de colunas numéricas;
- padronização de nomes de gêneros e artistas;
- criação de uma coluna de artista principal;
- tratamento da duração das músicas.

## 7. Transformação dos dados
Foram criadas novas variáveis para enriquecer a análise:

- `duration_min`: duração da música em minutos;
- `popularity_level`: classificação da popularidade em baixa, média e alta;
- `is_hit`: identificação de músicas com popularidade maior ou igual a 70;
- `music_profile`: classificação do perfil musical da faixa.

## 8. Dashboard 1 — Visão Geral
O primeiro dashboard apresenta uma visão executiva dos dados, com:

- total de músicas;
- total de artistas;
- popularidade média;
- gênero de destaque;
- top 10 gêneros por quantidade de músicas;
- top 10 gêneros por popularidade média;
- distribuição da popularidade;
- artistas com mais hits.

## 9. Dashboard 2 — Exploração Interativa
O segundo dashboard permite uma exploração mais detalhada, com filtros por:

- gênero;
- perfil musical;
- faixa de popularidade.

Ele possui visualizações como:

- popularidade x danceability;
- popularidade x energia;
- boxplot de popularidade por gênero;
- popularidade média por perfil musical;
- radar chart dos atributos musicais;
- matriz de correlação.

## 10. Principais insights esperados

### Insight 1 — Volume não significa maior popularidade
Alguns gêneros podem aparecer com grande quantidade de músicas, mas isso não significa que possuam a maior popularidade média.

### Insight 2 — Danceability pode influenciar o desempenho
Músicas com maior facilidade para dançar podem apresentar maior potencial de popularidade em alguns gêneros.

### Insight 3 — Energia e valence ajudam a caracterizar músicas populares
Faixas mais energéticas e com maior valence podem se destacar em determinados estilos musicais.

### Insight 4 — Nem todo artista com muitas músicas possui muitos hits
A quantidade de músicas publicadas por um artista não garante alta popularidade média.

### Insight 5 — Perfis musicais diferentes atraem públicos diferentes
Músicas acústicas, dançantes, positivas ou mais faladas possuem comportamentos distintos de popularidade.

## 11. Conclusão
O projeto demonstra como técnicas de ciência de dados podem ser utilizadas para compreender padrões no mercado musical. A análise permite identificar quais características estão mais associadas à popularidade e como diferentes gêneros e artistas se comportam dentro da base estudada.
