from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc

DATA_FILE = Path("data/processed/spotify_clean.csv")

if not DATA_FILE.exists():
    raise FileNotFoundError(
        "Arquivo data/processed/spotify_clean.csv não encontrado. "
        "Rode primeiro: python src/prepare_data.py"
    )

df = pd.read_csv(DATA_FILE)

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)

app.title = "Dashboard Spotify"

def kpi_card(title, value, subtitle=None):
    return dbc.Card(
        dbc.CardBody([
            html.Div(title, className="kpi-title"),
            html.H3(value, className="kpi-value"),
            html.Div(subtitle or "", className="kpi-subtitle")
        ]),
        className="kpi-card"
    )

def dashboard_geral():
    total_tracks = len(df)
    total_artists = df["main_artist"].nunique()
    avg_popularity = df["popularity"].mean()
    top_genre = (
        df.groupby("genre")["popularity"]
        .mean()
        .sort_values(ascending=False)
        .index[0]
    )
    hits = (df["is_hit"] == "Hit").sum()

    genre_count = df["genre"].value_counts().head(10).reset_index()
    genre_count.columns = ["genre", "qtd"]

    genre_pop = (
        df.groupby("genre")["popularity"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    profile_pop = (
        df.groupby("music_profile")["popularity"]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )

    artist_hits = (
        df[df["is_hit"] == "Hit"]
        .groupby("main_artist")["track_id"]
        .count()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    artist_hits.columns = ["main_artist", "hits"]

    fig_genre_count = px.bar(
        genre_count,
        x="qtd",
        y="genre",
        orientation="h",
        title="Top 10 gêneros com mais músicas",
        labels={"qtd": "Quantidade de músicas", "genre": "Gênero"}
    )
    fig_genre_count.update_layout(yaxis={"categoryorder": "total ascending"})

    fig_genre_pop = px.bar(
        genre_pop,
        x="popularity",
        y="genre",
        orientation="h",
        title="Top 10 gêneros por popularidade média",
        labels={"popularity": "Popularidade média", "genre": "Gênero"}
    )
    fig_genre_pop.update_layout(yaxis={"categoryorder": "total ascending"})

    fig_hist = px.histogram(
        df,
        x="popularity",
        nbins=30,
        title="Distribuição da popularidade das músicas",
        labels={"popularity": "Popularidade"}
    )

    fig_profile = px.bar(
        profile_pop,
        x="music_profile",
        y="popularity",
        title="Popularidade média por perfil musical",
        labels={"music_profile": "Perfil musical", "popularity": "Popularidade média"}
    )

    fig_artist_hits = px.bar(
        artist_hits,
        x="hits",
        y="main_artist",
        orientation="h",
        title="Top 10 artistas com mais hits",
        labels={"hits": "Quantidade de hits", "main_artist": "Artista"}
    )
    fig_artist_hits.update_layout(yaxis={"categoryorder": "total ascending"})

    return html.Div([
        html.H2("Dashboard 1 — Visão Geral", className="page-title"),
        html.P(
            "Painel executivo com os principais indicadores do dataset e os padrões gerais de popularidade.",
            className="page-description"
        ),

        dbc.Row([
            dbc.Col(kpi_card("Total de músicas", f"{total_tracks:,}".replace(",", ".")), md=3),
            dbc.Col(kpi_card("Total de artistas", f"{total_artists:,}".replace(",", ".")), md=3),
            dbc.Col(kpi_card("Popularidade média", f"{avg_popularity:.1f}"), md=3),
            dbc.Col(kpi_card("Gênero destaque", top_genre, f"{hits:,} hits no dataset".replace(",", ".")), md=3),
        ], className="mb-4"),

        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig_genre_count), md=6),
            dbc.Col(dcc.Graph(figure=fig_genre_pop), md=6),
        ]),

        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig_hist), md=6),
            dbc.Col(dcc.Graph(figure=fig_profile), md=6),
        ]),

        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig_artist_hits), md=12),
        ]),

        html.Div([
            html.H4("Principais interpretações"),
            html.Ul([
                html.Li("A visão geral permite identificar quais gêneros dominam em volume e quais possuem maior popularidade média."),
                html.Li("A distribuição de popularidade mostra se o dataset possui muitas músicas medianas ou concentração de hits."),
                html.Li("A comparação por perfil musical ajuda a entender quais características estão associadas a músicas mais populares.")
            ])
        ], className="insight-box")
    ])

def dashboard_exploracao():
    genres = sorted(df["genre"].dropna().unique())
    profiles = sorted(df["music_profile"].dropna().unique())

    return html.Div([
        html.H2("Dashboard 2 — Exploração Interativa", className="page-title"),
        html.P(
            "Área interativa para comparar gêneros, perfis musicais e atributos sonoros.",
            className="page-description"
        ),

        dbc.Card(
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.Label("Selecione os gêneros"),
                        dcc.Dropdown(
                            id="genre-filter",
                            options=[{"label": g, "value": g} for g in genres],
                            value=genres[:5],
                            multi=True
                        )
                    ], md=6),
                    dbc.Col([
                        html.Label("Selecione o perfil musical"),
                        dcc.Dropdown(
                            id="profile-filter",
                            options=[{"label": p, "value": p} for p in profiles],
                            value=profiles,
                            multi=True
                        )
                    ], md=3),
                    dbc.Col([
                        html.Label("Faixa de popularidade"),
                        dcc.RangeSlider(
                            id="popularity-filter",
                            min=0,
                            max=100,
                            step=1,
                            value=[0, 100],
                            marks={0: "0", 50: "50", 100: "100"}
                        )
                    ], md=3)
                ])
            ]),
            className="filter-card"
        ),

        dbc.Row([
            dbc.Col(dcc.Graph(id="scatter-dance"), md=6),
            dbc.Col(dcc.Graph(id="scatter-energy"), md=6),
        ]),

        dbc.Row([
            dbc.Col(dcc.Graph(id="box-genre"), md=6),
            dbc.Col(dcc.Graph(id="bar-profile"), md=6),
        ]),

        dbc.Row([
            dbc.Col(dcc.Graph(id="radar-features"), md=6),
            dbc.Col(dcc.Graph(id="corr-heatmap"), md=6),
        ]),

        html.Div(id="dynamic-insights", className="insight-box")
    ])

@app.callback(
    Output("scatter-dance", "figure"),
    Output("scatter-energy", "figure"),
    Output("box-genre", "figure"),
    Output("bar-profile", "figure"),
    Output("radar-features", "figure"),
    Output("corr-heatmap", "figure"),
    Output("dynamic-insights", "children"),
    Input("genre-filter", "value"),
    Input("profile-filter", "value"),
    Input("popularity-filter", "value"),
)
def update_exploration(selected_genres, selected_profiles, popularity_range):
    filtered = df.copy()

    if selected_genres:
        filtered = filtered[filtered["genre"].isin(selected_genres)]

    if selected_profiles:
        filtered = filtered[filtered["music_profile"].isin(selected_profiles)]

    filtered = filtered[
        (filtered["popularity"] >= popularity_range[0]) &
        (filtered["popularity"] <= popularity_range[1])
    ]

    if filtered.empty:
        empty_fig = px.scatter(title="Sem dados para os filtros selecionados")
        return empty_fig, empty_fig, empty_fig, empty_fig, empty_fig, empty_fig, html.P("Nenhum registro encontrado.")

    fig_scatter_dance = px.scatter(
        filtered.sample(min(len(filtered), 5000), random_state=42),
        x="danceability",
        y="popularity",
        color="genre",
        hover_data=["track_name", "main_artist"],
        title="Relação entre danceability e popularidade",
        labels={"danceability": "Danceability", "popularity": "Popularidade"}
    )

    fig_scatter_energy = px.scatter(
        filtered.sample(min(len(filtered), 5000), random_state=42),
        x="energy",
        y="popularity",
        color="music_profile",
        hover_data=["track_name", "main_artist"],
        title="Relação entre energia e popularidade",
        labels={"energy": "Energia", "popularity": "Popularidade"}
    )

    fig_box = px.box(
        filtered,
        x="genre",
        y="popularity",
        title="Distribuição de popularidade por gênero",
        labels={"genre": "Gênero", "popularity": "Popularidade"}
    )

    profile_summary = (
        filtered.groupby("music_profile")["popularity"]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig_bar_profile = px.bar(
        profile_summary,
        x="music_profile",
        y="popularity",
        title="Popularidade média por perfil musical",
        labels={"music_profile": "Perfil musical", "popularity": "Popularidade média"}
    )

    radar_cols = ["danceability", "energy", "valence", "acousticness", "speechiness"]
    radar_values = filtered[radar_cols].mean().values.tolist()
    radar_labels = ["Danceability", "Energia", "Valence", "Acousticness", "Speechiness"]

    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=radar_values + [radar_values[0]],
        theta=radar_labels + [radar_labels[0]],
        fill="toself",
        name="Média dos atributos"
    ))
    fig_radar.update_layout(
        title="Perfil médio dos atributos musicais",
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=False
    )

    corr_cols = ["popularity", "danceability", "energy", "valence", "acousticness", "speechiness", "tempo", "duration_min"]
    corr = filtered[corr_cols].corr(numeric_only=True)

    fig_corr = px.imshow(
        corr,
        text_auto=True,
        title="Correlação entre variáveis",
        labels=dict(color="Correlação")
    )

    avg_pop = filtered["popularity"].mean()
    top_genre = filtered.groupby("genre")["popularity"].mean().sort_values(ascending=False).index[0]
    top_profile = filtered.groupby("music_profile")["popularity"].mean().sort_values(ascending=False).index[0]

    insights = html.Div([
        html.H4("Insights com os filtros selecionados"),
        html.Ul([
            html.Li(f"Foram analisadas {len(filtered):,} músicas dentro dos filtros selecionados.".replace(",", ".")),
            html.Li(f"A popularidade média do recorte é {avg_pop:.1f}."),
            html.Li(f"O gênero com maior popularidade média no recorte é {top_genre}."),
            html.Li(f"O perfil musical com maior popularidade média é {top_profile}."),
            html.Li("Use os gráficos de dispersão para observar se danceability e energia se relacionam com músicas mais populares.")
        ])
    ])

    return fig_scatter_dance, fig_scatter_energy, fig_box, fig_bar_profile, fig_radar, fig_corr, insights

app.layout = dbc.Container([
    html.Div([
        html.H1("Análise de Tendências Musicais no Spotify"),
        html.P("Dashboard interativo desenvolvido com Python, Pandas, Plotly e Dash.")
    ], className="header"),

    dcc.Tabs(
        id="tabs",
        value="geral",
        children=[
            dcc.Tab(label="Dashboard 1 — Visão Geral", value="geral"),
            dcc.Tab(label="Dashboard 2 — Exploração Interativa", value="exploracao"),
        ]
    ),

    html.Div(id="tab-content")
], fluid=True)

@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "value")
)
def render_tab(tab):
    if tab == "geral":
        return dashboard_geral()
    return dashboard_exploracao()

if __name__ == "__main__":
    app.run(debug=True) 
