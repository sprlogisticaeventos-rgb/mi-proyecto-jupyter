# ============================
# DASHBOARD FORUS INTERACTIVO - FINAL 2025 (JUPYTER + APP READY)
# ============================

import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Input, Output
import pycountry

# ---------------------------
# FUNCIONES AUXILIARES
# ---------------------------
def get_iso3(country):
    """Convierte nombres de país a código ISO-3 (para el mapa)."""
    try:
        return pycountry.countries.lookup(country).alpha_3
    except:
        return None


def kpi_card(title, value, color, id):
    """Crea tarjetas de KPI con color personalizado."""
    return dbc.Card(
        [
            html.H5(title, className="card-title", style={"color": "#fff"}),
            html.H2(value, className="card-text", id=id, style={"color": "#fff"}),
        ],
        body=True,
        style={
            "backgroundColor": color,
            "border": "none",
            "borderRadius": "15px",
            "textAlign": "center",
            "marginBottom": "10px",
        },
    )


def module_card(icon_src, title, count_id, accent_color):
    """Crea tarjetas de módulo con ícono SVG y contador dinámico."""
    return html.Div(
        [
            html.Img(src=icon_src, style={"width": "50px", "height": "50px"}),
            html.Div(
                [
                    html.Div(title, className="module-title", style={"color": accent_color}),
                    html.Div("0 people", id=count_id, className="module-count"),
                ]
            ),
        ],
        className="module-card",
    )


# ---------------------------
# CARGA DE DATOS
# ---------------------------
df = pd.read_csv("BaseLimpia_2025-10-30.csv")
df.columns = df.columns.str.lower()
df["email"] = df["email"].str.strip().str.lower()

follow_df = pd.read_excel(
    "/Users/santiagopulgarinrodriguez/Downloads/Forus Participants 2025.xlsx",
    sheet_name="Follow-up Comms",
    header=1,
)
follow_df.columns = [
    "participant",
    "modules",
    "group",
    "phone",
    "email",
    "mail_date",
    "profiling_status",
    "poke_date",
    "registration_date",
]
follow_df = follow_df.dropna(subset=["email"]).reset_index(drop=True)
follow_df["email"] = follow_df["email"].str.strip().str.lower()
follow_df["profiling_status"] = (
    follow_df["profiling_status"].fillna("Pending").str.strip().str.capitalize()
)
follow_df["registration_date"] = pd.to_datetime(
    follow_df["registration_date"], errors="coerce"
)

# Unión
merged_df = df.merge(
    follow_df[["email", "profiling_status", "registration_date"]],
    on="email",
    how="left",
)

# ---------------------------
# COLORES
# ---------------------------
color_bg = "#f2f2f2"
color_red = "#ed1b2e"
color_green = "#00b1a9"
color_yellow = "#f2b124"
color_dark = "#333333"

# ---------------------------
# INICIALIZAR APP
# ---------------------------
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], assets_folder="assets")
app.title = "Forus Learning Modules Dashboard"

# ---------------------------
# LAYOUT FINAL
# ---------------------------
app.layout = dbc.Container(
    [
        html.Div(
            html.H2(
                "Forus Learning Modules Dashboard",
                style={
                    "backgroundColor": "#404040",
                    "color": "white",
                    "padding": "15px",
                    "borderRadius": "8px",
                    "textAlign": "center",
                    "fontWeight": "bold",
                    "fontFamily": "Arial",
                },
            ),
            style={"marginBottom": "25px"},
        ),

        dbc.Row(
            [
                # KPIs a la izquierda
                dbc.Col(
                    [
                        kpi_card("👥 Total people enrolled", "123", color_red, "kpi-total"),
                        kpi_card(
                            "📚 People taking more than one module",
                            "29",
                            color_dark,
                            "kpi-multi",
                        ),
                        kpi_card(
                            "🧩 Profiled individuals", "24", color_green, "kpi-profiled"
                        ),
                        kpi_card(
                            "✅ Confirmed attendees",
                            "118",
                            color_yellow,
                            "kpi-confirmed",
                        ),
                    ],
                    width=2,
                    style={"paddingRight": "10px"},
                ),

                # Contenido principal
                dbc.Col(
                    [
                        # FILTROS
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Label(
                                            "Filter by Module",
                                            style={"fontWeight": "bold"},
                                        ),
                                        dcc.Dropdown(
                                            id="theme-filter",
                                            options=[
                                                {"label": t, "value": t}
                                                for t in sorted(df["theme"].unique())
                                            ],
                                            placeholder="Select module",
                                        ),
                                    ],
                                    width=4,
                                ),
                                dbc.Col(
                                    [
                                        html.Label(
                                            "Filter by Language",
                                            style={"fontWeight": "bold"},
                                        ),
                                        dcc.Dropdown(
                                            id="lang-filter",
                                            options=[
                                                {"label": l, "value": l}
                                                for l in sorted(df["language"].unique())
                                            ],
                                            placeholder="Select language",
                                        ),
                                    ],
                                    width=4,
                                ),
                                dbc.Col(
                                    [
                                        html.Label(
                                            "Filter by Role",
                                            style={"fontWeight": "bold"},
                                        ),
                                        dcc.Dropdown(
                                            id="role-filter",
                                            options=[
                                                {"label": r, "value": r}
                                                for r in sorted(
                                                    df["position_group"].unique()
                                                )
                                            ],
                                            placeholder="Select role",
                                        ),
                                    ],
                                    width=4,
                                ),
                            ],
                            style={"marginBottom": "25px"},
                        ),

                        # Módulos con íconos SVG
                        html.Div(
                            [
                                html.H4(
                                    "Enrolled people per module",
                                    style={
                                        "fontWeight": "bold",
                                        "marginBottom": "15px",
                                        "color": "#333",
                                    },
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            module_card(
                                                "assets/icons/ai.svg",
                                                "NGO Management & AI Ethics",
                                                "count-ai",
                                                "#00b1a9",
                                            ),
                                            width=6,
                                        ),
                                        dbc.Col(
                                            module_card(
                                                "assets/icons/security.svg",
                                                "Digital Security & Risk Management",
                                                "count-sec",
                                                "#007bff",
                                            ),
                                            width=6,
                                        ),
                                    ],
                                    style={"marginBottom": "12px"},
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            module_card(
                                                "assets/icons/funding.svg",
                                                "Resource Mobilization for CSO",
                                                "count-res",
                                                "#f2b124",
                                            ),
                                            width=6,
                                        ),
                                        dbc.Col(
                                            module_card(
                                                "assets/icons/speaking.svg",
                                                "Public Speaking for Global Leaders",
                                                "count-pub",
                                                "#ed1b2e",
                                            ),
                                            width=6,
                                        ),
                                    ]
                                ),
                            ],
                            style={
                                "backgroundColor": "#fff",
                                "padding": "25px",
                                "borderRadius": "12px",
                                "boxShadow": "0 3px 6px rgba(0,0,0,0.1)",
                                "marginBottom": "25px",
                            },
                        ),

                        # Gráficos
                        dbc.Row(
                            [
                                dbc.Col(dcc.Graph(id="bar-theme"), width=6),
                                dbc.Col(dcc.Graph(id="pie-role"), width=6),
                            ]
                        ),

                        # Mapa centrado
                        dbc.Row(
                            [
                                dbc.Col(
                                    dcc.Graph(
                                        id="map-country",
                                        style={
                                            "height": "600px",
                                            "marginTop": "25px",
                                            "marginBottom": "20px",
                                            "boxShadow": "0 3px 6px rgba(0,0,0,0.1)",
                                            "borderRadius": "10px",
                                            "backgroundColor": "#fff",
                                        },
                                    ),
                                    width={"size": 10, "offset": 1},
                                ),
                            ]
                        ),
                    ],
                    width=10,
                ),
            ]
        ),
    ],
    fluid=True,
    style={
        "backgroundColor": "#f2f2f2",
        "padding": "20px",
        "fontFamily": "Arial",
    },
)


# ---------------------------
# CALLBACKS
# ---------------------------
@app.callback(
    [
        Output("bar-theme", "figure"),
        Output("pie-role", "figure"),
        Output("map-country", "figure"),
        Output("kpi-total", "children"),
        Output("kpi-multi", "children"),
        Output("kpi-profiled", "children"),
        Output("kpi-confirmed", "children"),
        Output("count-ai", "children"),
        Output("count-sec", "children"),
        Output("count-res", "children"),
        Output("count-pub", "children"),
    ],
    [
        Input("theme-filter", "value"),
        Input("lang-filter", "value"),
        Input("role-filter", "value"),
    ],
)
def update_graphs(theme_value, lang_value, role_value):
    dff = merged_df.copy()
    if theme_value:
        dff = dff[dff["theme"] == theme_value]
    if lang_value:
        dff = dff[dff["language"] == lang_value]
    if role_value:
        dff = dff[dff["position_group"] == role_value]

    unique_filtered = (
        dff.groupby("email")
        .agg(
            {
                "theme": lambda x: ", ".join(sorted(x.unique())),
                "profiling_status": "first",
                "registration_date": "first",
            }
        )
        .reset_index()
    )
    total_people = unique_filtered["email"].nunique()
    multi_module = unique_filtered["theme"].str.contains(",").sum()
    profiled = (unique_filtered["profiling_status"] == "Completed").sum()
    confirmed = unique_filtered["registration_date"].notna().sum()

    c_ai = (dff["theme"] == "Ai For Ngos").sum()
    c_sec = (dff["theme"] == "Digital Security").sum()
    c_res = (dff["theme"] == "Resource Mobilization").sum()
    c_pub = (dff["theme"] == "Public Speaking").sum()

    theme_counts = dff["theme"].value_counts().reset_index()
    theme_counts.columns = ["theme", "count"]
    bar_fig = px.bar(
        theme_counts,
        x="theme",
        y="count",
        color_discrete_sequence=[color_green],
        title="Participants per Module",
    )
    bar_fig.update_layout(
        xaxis_title="Module",
        yaxis_title="Count",
        plot_bgcolor=color_bg,
        paper_bgcolor=color_bg,
    )

    pie_fig = px.pie(
        dff,
        names="position_group",
        color_discrete_sequence=px.colors.qualitative.Pastel,
        title="Role Distribution",
    )
    pie_fig.update_layout(plot_bgcolor=color_bg, paper_bgcolor=color_bg)

    country_counts = dff["country"].value_counts().reset_index()
    country_counts.columns = ["country", "count"]
    country_counts["iso3"] = country_counts["country"].apply(get_iso3)
    map_fig = px.choropleth(
        country_counts.dropna(subset=["iso3"]),
        locations="iso3",
        color="count",
        color_continuous_scale=["#f2b124", "#ed1b2e"],
        title="Country Distribution",
    )
    map_fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type="natural earth",
            center=dict(lat=5, lon=10),
            fitbounds="locations",
        ),
        plot_bgcolor=color_bg,
        paper_bgcolor=color_bg,
    )

    return (
        bar_fig,
        pie_fig,
        map_fig,
        str(total_people),
        str(multi_module),
        str(profiled),
        str(confirmed),
        f"{c_ai} people",
        f"{c_sec} people",
        f"{c_res} people",
        f"{c_pub} people",
    )


# ---------------------------
# RUN (JUPYTER o APP)
# ---------------------------
if __name__ == "__main__":
    # MODO JUPYTER:
    # app.run(mode="inline")

    # MODO APLICACIÓN (pestaña del navegador):
    app.run(debug=True)
