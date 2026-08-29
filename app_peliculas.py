import os
import json
import html
import requests
import streamlit as st

# ============================================================
# CONFIGURACIÓN
# ============================================================
st.set_page_config(
    page_title="CineVega",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

TMDB_API_KEY = os.getenv("TMDB_API_KEY", "8a5fe9643d4410984062cd935e4a8fa7")
TMDB_BASE = "https://api.themoviedb.org/3"
POSTER_BASE = "https://image.tmdb.org/t/p/w500"
BACKDROP_BASE = "https://image.tmdb.org/t/p/w1280"
PLACEHOLDER = "https://via.placeholder.com/500x750/12131a/777777?text=Sin+poster"
DATA_FILE = "datos_cinevega.json"


# ============================================================
# ESTÉTICA
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #08090d;
    --panel: #11131a;
    --panel2: #171a23;
    --text: #f5f5f7;
    --muted: #9297a5;
    --accent: #e50914;
    --accent2: #8b5cf6;
    --line: rgba(255,255,255,.08);
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 80% -10%, rgba(139,92,246,.18), transparent 30%),
        radial-gradient(circle at 5% 10%, rgba(229,9,20,.10), transparent 28%),
        var(--bg);
    color: var(--text);
}

header[data-testid="stHeader"] {
    background: transparent;
}
header[data-testid="stHeader"] svg {
    fill: #e5e5e5;
}

#MainMenu, footer { visibility: hidden; }

.block-container {
    max-width: 1500px;
    padding-top: 1.8rem;
    padding-bottom: 4rem;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d0f15 0%, #090a0f 100%);
    border-right: 1px solid var(--line);
}

section[data-testid="stSidebar"] .stRadio label {
    padding: 11px 14px;
    border-radius: 10px;
    transition: .2s ease;
    border-left: 3px solid transparent;
}

section[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(139,92,246,.10);
}

section[data-testid="stSidebar"] .stRadio label:has(input:checked) {
    background: linear-gradient(90deg, rgba(229,9,20,.18), rgba(139,92,246,.12));
    border-left-color: var(--accent);
}

section[data-testid="stSidebar"] .stRadio label > div:first-child {
    display: none !important;
}

section[data-testid="stSidebar"] .stRadio p {
    font-weight: 600;
}

/* Header */
.brand {
    position: relative;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,.08);
    border-radius: 22px;
    padding: 28px 32px;
    margin-bottom: 24px;
    background:
        linear-gradient(115deg, rgba(229,9,20,.92), rgba(107,38,180,.88)),
        #181922;
    box-shadow: 0 20px 60px rgba(0,0,0,.32);
}

.brand:after {
    content: "";
    position: absolute;
    width: 360px;
    height: 360px;
    right: -130px;
    top: -220px;
    border-radius: 50%;
    border: 60px solid rgba(255,255,255,.07);
}

.brand h1 {
    margin: 0;
    color: white;
    font-size: 2.35rem;
    font-weight: 800;
    letter-spacing: -1.5px;
    position: relative;
    z-index: 2;
}

.brand p {
    margin: 5px 0 0;
    color: rgba(255,255,255,.82);
    position: relative;
    z-index: 2;
}

/* Hero */
.hero {
    min-height: 360px;
    border-radius: 22px;
    overflow: hidden;
    position: relative;
    background-size: cover;
    background-position: center;
    margin: 10px 0 28px;
    box-shadow: 0 22px 60px rgba(0,0,0,.45);
    border: 1px solid rgba(255,255,255,.07);
}

.hero:after {
    content: "";
    position: absolute;
    inset: 0;
    background:
        linear-gradient(90deg, rgba(5,6,9,.96) 0%, rgba(5,6,9,.70) 40%, rgba(5,6,9,.15) 80%),
        linear-gradient(0deg, rgba(5,6,9,.65), transparent 55%);
}

.hero-content {
    position: absolute;
    z-index: 2;
    left: 34px;
    bottom: 30px;
    max-width: 620px;
}

.hero-kicker {
    display: inline-block;
    padding: 6px 11px;
    border-radius: 999px;
    background: rgba(229,9,20,.9);
    color: white;
    font-size: .72rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: .8px;
}

.hero h2 {
    color: white;
    font-size: 2.45rem;
    line-height: 1.05;
    margin: 10px 0 8px;
}

.hero p {
    color: rgba(255,255,255,.82);
    margin: 0;
}

/* Cards */
.movie-card {
    background: linear-gradient(160deg, #181b25, #101219);
    border: 1px solid var(--line);
    border-radius: 16px;
    overflow: hidden;
    padding-bottom: 10px;
    transition: transform .2s ease, box-shadow .2s ease, border-color .2s ease;
    height: 100%;
}

.movie-card:hover {
    transform: translateY(-6px);
    border-color: rgba(139,92,246,.45);
    box-shadow: 0 18px 38px rgba(0,0,0,.40);
}

.poster-wrap img {
    width: 100%;
    aspect-ratio: 2 / 3;
    object-fit: cover;
    display: block;
}

.movie-info {
    padding: 10px 12px 4px;
}

.movie-title {
    color: #f4f4f5;
    font-size: .90rem;
    font-weight: 700;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.movie-meta {
    color: #8f95a3;
    font-size: .75rem;
    margin-top: 4px;
}

.rating {
    color: #f6c945;
    font-weight: 700;
}

/* Ficha */
.detail-panel {
    background: linear-gradient(150deg, #181b25, #101219);
    border: 1px solid var(--line);
    border-radius: 20px;
    padding: 22px;
    box-shadow: 0 15px 45px rgba(0,0,0,.28);
}

.stat {
    background: #11131a;
    border: 1px solid var(--line);
    border-radius: 12px;
    padding: 11px 14px;
    margin-bottom: 8px;
}

.stat-label {
    color: var(--muted);
    font-size: .70rem;
    display: block;
}

.stat-value {
    color: white;
    font-size: 1rem;
    font-weight: 700;
}

/* Botones */
.stButton > button {
    border-radius: 10px;
    min-height: 40px;
    font-weight: 700;
    transition: .18s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
}

button[kind="primary"] {
    background: linear-gradient(120deg, #e50914, #8b5cf6) !important;
    border: 0 !important;
}

button[kind="secondary"] {
    background: rgba(255,255,255,.045) !important;
    border: 1px solid rgba(255,255,255,.11) !important;
    color: #eee !important;
}

button[kind="secondary"]:hover {
    background: rgba(139,92,246,.16) !important;
    border-color: rgba(139,92,246,.55) !important;
}

/* Inputs */
div[data-baseweb="select"] > div,
.stTextInput input,
.stNumberInput input,
.stTextArea textarea {
    background: #11131a !important;
    border: 1px solid rgba(255,255,255,.09) !important;
    border-radius: 10px !important;
}

/* Métricas */
div[data-testid="stMetric"] {
    background: linear-gradient(150deg, #171a22, #101219);
    border: 1px solid var(--line);
    border-radius: 15px;
    padding: 15px;
}

/* Separadores y títulos */
hr {
    border-color: var(--line) !important;
}

h1, h2, h3, h4 {
    letter-spacing: -.4px;
}

/* Menú lateral estilo Kick: ítem activo resaltado, texto+ícono alineados a la izquierda */
section[data-testid="stSidebar"] button[kind] {
    border-radius: 10px !important;
    padding: 10px 14px !important;
    margin-bottom: 2px !important;
    font-weight: 600 !important;
    justify-content: flex-start !important;
}
section[data-testid="stSidebar"] button[kind] div[data-testid="stMarkdownContainer"] {
    text-align: left !important;
}
section[data-testid="stSidebar"] button[kind="secondary"] {
    background: transparent !important;
    border: none !important;
    color: #aab0c4 !important;
}
section[data-testid="stSidebar"] button[kind="secondary"]:hover {
    background: rgba(255,255,255,0.06) !important;
    color: white !important;
}
section[data-testid="stSidebar"] button[kind="primary"] {
    background: linear-gradient(120deg, rgba(229,9,20,0.22), rgba(139,92,246,0.28)) !important;
    border: 1px solid rgba(139,92,246,0.45) !important;
    color: white !important;
}

/* Botón propio para abrir/cerrar el menú (reemplaza al control nativo, que no se pudo restylear).
   .st-key-toggle_sidebar_wrap es la clase real que Streamlit genera a partir del key
   del contenedor, así que este selector sí va a encontrar el elemento.
   position:fixed lo pega al borde real de la pantalla, sin importar el margen del contenido. */
.st-key-toggle_sidebar_wrap {
    position: fixed !important;
    top: 12px !important;
    left: 12px !important;
    z-index: 1000000 !important;
    width: auto !important;
}
.st-key-toggle_sidebar_wrap button {
    background: rgba(139, 92, 246, 0.35) !important;
    border: 1px solid rgba(139, 92, 246, 0.5) !important;
    border-radius: 8px !important;
    width: 42px !important;
    padding: 8px !important;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# DATOS
# ============================================================
def cargar_datos():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception:
        return []


def guardar_datos():
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(st.session_state.peliculas, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def compactar_html(codigo_html):
    """Saca la sangría de cada línea para que Streamlit/Markdown no la confunda con un bloque de código."""
    return "\n".join(linea.strip() for linea in codigo_html.strip().splitlines())


def existe_titulo(titulo, ignorar=None):
    return any(
        i != ignorar and p.get("titulo", "").strip().lower() == titulo.strip().lower()
        for i, p in enumerate(st.session_state.peliculas)
    )


# ============================================================
# TMDB
# ============================================================
@st.cache_data(ttl=600, show_spinner=False)
def tmdb_get(endpoint, params=None):
    try:
        params = params or {}
        params["api_key"] = TMDB_API_KEY
        r = requests.get(
            f"{TMDB_BASE}/{endpoint}",
            params=params,
            timeout=8,
        )
        r.raise_for_status()
        return r.json()
    except Exception:
        return None


def buscar_tmdb(query, pagina=1):
    if not query.strip():
        return {"results": [], "total_pages": 0}
    return tmdb_get(
        "search/movie",
        {
            "query": query,
            "language": "es-419",
            "include_adult": False,
            "page": pagina,
        },
    ) or {"results": [], "total_pages": 0}


def populares_tmdb(pagina=1):
    return tmdb_get(
        "movie/popular",
        {
            "language": "es-419",
            "region": "AR",
            "page": pagina,
        },
    ) or {"results": [], "total_pages": 0}


@st.cache_data(ttl=86400, show_spinner=False)
def generos_tmdb():
    data = tmdb_get("genre/movie/list", {"language": "es-419"}) or {}
    return {g["name"]: g["id"] for g in data.get("genres", [])}


def descubrir_tmdb(genero_id=None, pagina=1):
    params = {
        "language": "es-419",
        "sort_by": "popularity.desc",
        "page": pagina,
        "include_adult": False,
    }
    if genero_id:
        params["with_genres"] = genero_id
    return tmdb_get("discover/movie", params) or {"results": [], "total_pages": 0}


def detalle_tmdb(movie_id):
    return tmdb_get(
        f"movie/{movie_id}",
        {
            "language": "es-419",
            "append_to_response": "credits",
        },
    ) or {}


def convertir_pelicula(resultado, detalle=None):
    detalle = detalle or detalle_tmdb(resultado["id"])

    poster = resultado.get("poster_path")
    backdrop = detalle.get("backdrop_path") or resultado.get("backdrop_path")

    generos = ", ".join(
        g.get("name", "") for g in detalle.get("genres", []) if g.get("name")
    ) or "Sin género"

    return {
        "tmdb_id": resultado.get("id"),
        "titulo": resultado.get("title") or resultado.get("original_title") or "Sin título",
        "genero": generos,
        "duracion": detalle.get("runtime") or 0,
        "recaudacion": detalle.get("revenue") or 0,
        "poster": POSTER_BASE + poster if poster else None,
        "backdrop": BACKDROP_BASE + backdrop if backdrop else (POSTER_BASE + poster if poster else None),
        "tmdb_rating": round(float(resultado.get("vote_average") or detalle.get("vote_average") or 0), 1),
        "tmdb_votes": int(resultado.get("vote_count") or detalle.get("vote_count") or 0),
        "descripcion": detalle.get("overview") or resultado.get("overview") or "",
        "puntaje": 5,
        "comentario": "",
        "calificada": False,
        "para_despues": False,
    }


# ============================================================
# ESTADO
# ============================================================
if "peliculas" not in st.session_state:
    st.session_state.peliculas = cargar_datos()

if "pagina_populares" not in st.session_state:
    st.session_state.pagina_populares = 1

if "pagina_busqueda" not in st.session_state:
    st.session_state.pagina_busqueda = 1

if "busqueda_actual" not in st.session_state:
    st.session_state.busqueda_actual = ""

if "pelicula_activa" not in st.session_state:
    st.session_state.pelicula_activa = None

if "match_deck" not in st.session_state:
    st.session_state.match_deck = []

if "match_pagina" not in st.session_state:
    st.session_state.match_pagina = 1

if "match_genero" not in st.session_state:
    st.session_state.match_genero = "Todos"


def encontrar_pelicula(titulo):
    for p in st.session_state.peliculas:
        if p.get("titulo") == titulo:
            return p
    return None


# ============================================================
# COMPONENTES
# ============================================================
def poster_url(p):
    return p.get("poster") or PLACEHOLDER


def mostrar_hero(p, etiqueta):
    imagen = p.get("backdrop") or p.get("poster")
    if not imagen:
        return

    titulo = html.escape(p.get("titulo", ""))
    genero = html.escape(p.get("genero", "Sin género"))
    detalle = f"{p.get('duracion', 0)} min"

    st.markdown(
        compactar_html(f"""
        <div class="hero" style="background-image:url('{imagen}')">
            <div class="hero-content">
                <span class="hero-kicker">{html.escape(etiqueta)}</span>
                <h2>{titulo}</h2>
                <p>{genero} · {detalle} · TMDb {p.get('tmdb_rating', 0)}/10</p>
            </div>
        </div>
        """),
        unsafe_allow_html=True,
    )


def render_grid(lista, key_prefix, columnas=6):
    if not lista:
        st.info("No hay películas para mostrar con estos filtros.")
        return

    for inicio in range(0, len(lista), columnas):
        fila = lista[inicio:inicio + columnas]
        cols = st.columns(columnas)

        for pos, (col, p) in enumerate(zip(cols, fila)):
            with col:
                titulo = html.escape(p.get("titulo", "Sin título"))
                rating = p.get("tmdb_rating", 0)

                extra_puntaje = ""
                if p.get("calificada"):
                    tu_puntaje = p.get("puntaje", 5)
                    extra_puntaje = f" · Tu {tu_puntaje}/10"

                st.markdown(
                    compactar_html(f"""
                    <div class="movie-card">
                        <div class="poster-wrap">
                            <img src="{poster_url(p)}">
                        </div>
                        <div class="movie-info">
                            <div class="movie-title" title="{titulo}">{titulo}</div>
                            <div class="movie-meta">
                                <span class="rating">{rating}/10</span>{extra_puntaje}
                            </div>
                        </div>
                    </div>
                    """),
                    unsafe_allow_html=True,
                )

                identificador = p.get("tmdb_id") or f"{p.get('titulo','')}_{inicio}_{pos}"

                if st.button(
                    "Abrir ficha",
                    key=f"{key_prefix}_{identificador}",
                    use_container_width=True,
                ):
                    if not existe_titulo(p.get("titulo", "")):
                        nueva = {k: v for k, v in p.items() if k != "_resultado_tmdb"}
                        st.session_state.peliculas.append(nueva)
                        guardar_datos()
                    st.session_state.pelicula_activa = p.get("titulo")
                    st.rerun()


def render_ficha(p):
    if st.button("Volver al catálogo", use_container_width=False):
        st.session_state.pelicula_activa = None
        st.rerun()

    imagen = p.get("backdrop") or p.get("poster")
    if imagen:
        st.markdown(
            compactar_html(f"""
            <div class="hero" style="height:300px;background-image:url('{imagen}')">
                <div class="hero-content">
                    <span class="hero-kicker">Ficha de película</span>
                    <h2>{html.escape(p.get('titulo',''))}</h2>
                    <p>{html.escape(p.get('genero','Sin género'))} · {p.get('duracion',0)} min</p>
                </div>
            </div>
            """),
            unsafe_allow_html=True,
        )

    col_img, col_info = st.columns([1, 2], gap="large")

    with col_img:
        st.image(poster_url(p), use_container_width=True)

    with col_info:
        st.markdown('<div class="detail-panel">', unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)

        c1.markdown(
            f'<div class="stat"><span class="stat-label">TMDb</span>'
            f'<span class="stat-value">{p.get("tmdb_rating",0)}/10</span></div>',
            unsafe_allow_html=True,
        )
        c2.markdown(
            f'<div class="stat"><span class="stat-label">Tu puntuación</span>'
            f'<span class="stat-value">{p.get("puntaje",5)}/10</span></div>',
            unsafe_allow_html=True,
        )
        c3.markdown(
            f'<div class="stat"><span class="stat-label">Votos TMDb</span>'
            f'<span class="stat-value">{p.get("tmdb_votes",0):,}</span></div>',
            unsafe_allow_html=True,
        )

        st.markdown("### Sinopsis")
        st.write(p.get("descripcion") or "No hay sinopsis disponible.")

        st.markdown("### Tu reseña")

        with st.form(f"form_{p.get('titulo')}"):
            nuevo_puntaje = st.slider(
                "Puntuación",
                min_value=1,
                max_value=10,
                value=int(p.get("puntaje", 5)),
            )
            nuevo_comentario = st.text_area(
                "Comentario",
                value=p.get("comentario", ""),
                placeholder="Escribí qué te pareció la película...",
                height=130,
            )

            guardar = st.form_submit_button(
                "Guardar cambios",
                type="primary",
                use_container_width=True,
            )

        if guardar:
            p["puntaje"] = nuevo_puntaje
            p["comentario"] = nuevo_comentario
            p["calificada"] = True
            guardar_datos()
            st.success("La reseña fue guardada.")
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

        st.write("")

        if st.button(
            "Quitar de mi catálogo",
            key=f"delete_{p.get('titulo')}",
            use_container_width=True,
        ):
            st.session_state.peliculas = [
                x for x in st.session_state.peliculas
                if x.get("titulo") != p.get("titulo")
            ]
            guardar_datos()
            st.session_state.pelicula_activa = None
            st.rerun()


# ============================================================
# BOTÓN PROPIO PARA ABRIR/CERRAR EL MENÚ
# (reemplaza al control nativo de Streamlit, que no se puede restylear de forma confiable)
# ============================================================
if "sidebar_abierta" not in st.session_state:
    st.session_state.sidebar_abierta = True

with st.container(key="toggle_sidebar_wrap"):
    if st.button("", icon=":material/menu:", key="toggle_sidebar_custom"):
        st.session_state.sidebar_abierta = not st.session_state.sidebar_abierta
        st.rerun()

if st.session_state.sidebar_abierta:
    st.markdown(
        """
        <style>
        section[data-testid='stSidebar'] {
            display: block !important;
            visibility: visible !important;
            transform: none !important;
            width: 21rem !important;
            min-width: 21rem !important;
            margin-left: 0 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        "<style>section[data-testid='stSidebar']{display:none !important;}</style>",
        unsafe_allow_html=True,
    )

# Se oculta toda la barra superior nativa de Streamlit (donde vivían los controles
# viejos de abrir/cerrar) porque ya no la necesitamos: el único control es el nuestro.
st.markdown(
    """
    <style>
    header[data-testid="stHeader"] {
        display: none !important;
    }
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="stSidebarCollapseButton"],
    [data-testid="collapsedControl"],
    [data-testid="baseButton-headerNoPadding"],
    [aria-label="Open sidebar"],
    [aria-label="Close sidebar"],
    [aria-label="Expand sidebar"],
    [aria-label="Collapse sidebar"] {
        display: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# HEADER
# ============================================================
st.markdown("""
<div class="brand">
    <h1>CineVega</h1>
    <p>Tu catálogo personal. Descubrí, calificá y organizá tus películas.</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================
st.sidebar.markdown(
    compactar_html("""
    <div style="margin-bottom: 4px;">
        <h2 style="margin:0; font-size:1.4rem;">CineVega</h2>
        <p style="margin:0; font-size:0.78rem; letter-spacing:0.5px; text-transform:uppercase;
                  color:#9aa0b8; font-weight:600;">Descubrí y calificá películas</p>
    </div>
    """),
    unsafe_allow_html=True,
)
st.sidebar.write("")

NAV_ITEMS = [
    ("Inicio", "home"),
    ("CineMatch", "swipe"),
    ("Mi colección", "favorite"),
    ("Buscar", "search"),
    ("Estadísticas", "bar_chart"),
    ("Agregar película", "add_circle"),
]

if "menu_principal" not in st.session_state:
    st.session_state.menu_principal = "Inicio"

for etiqueta, icono in NAV_ITEMS:
    activo = st.session_state.menu_principal == etiqueta
    if st.sidebar.button(
        etiqueta,
        icon=f":material/{icono}:",
        key=f"nav_{etiqueta}",
        use_container_width=True,
        type="primary" if activo else "secondary",
    ):
        st.session_state.menu_principal = etiqueta
        st.rerun()

menu = st.session_state.menu_principal


# ============================================================
# FICHA ACTIVA
# ============================================================
pelicula_activa = (
    encontrar_pelicula(st.session_state.pelicula_activa)
    if st.session_state.pelicula_activa
    else None
)

if pelicula_activa:
    render_ficha(pelicula_activa)

# ============================================================
# INICIO
# ============================================================
elif menu == "Inicio":
    data = populares_tmdb(st.session_state.pagina_populares)
    resultados = data.get("results", [])
    total_pages = min(data.get("total_pages", 1), 500)

    if resultados:
        destacada = convertir_pelicula(resultados[0])
        mostrar_hero(destacada, "Popular ahora")

        render_grid(
            [{**convertir_pelicula(r), "_resultado_tmdb": True} for r in resultados],
            "inicio",
        )

        st.divider()

        c1, c2 = st.columns([1, 1])
        with c1:
            if st.session_state.pagina_populares > 1:
                if st.button("Página anterior", use_container_width=True):
                    st.session_state.pagina_populares -= 1
                    st.rerun()
        with c2:
            if st.button(
                "Cargar siguiente página",
                type="primary",
                use_container_width=True,
                disabled=st.session_state.pagina_populares >= total_pages,
            ):
                st.session_state.pagina_populares += 1
                st.rerun()
    else:
        st.warning("No se pudo cargar el catálogo de TMDb. Revisá la API o la conexión.")


# ============================================================
# CINEMATCH: descubrí películas al estilo swipe
# ============================================================
elif menu == "CineMatch":
    st.subheader("CineMatch")
    st.caption("Te mostramos una película a la vez. ✖ para pasar, ❤ para guardarla y verla más tarde.")

    mapa_generos = generos_tmdb()
    opciones_genero = ["Todos"] + sorted(mapa_generos.keys())

    if st.session_state.match_genero not in opciones_genero:
        st.session_state.match_genero = "Todos"

    genero_elegido = st.selectbox(
        "Filtrar por género",
        opciones_genero,
        index=opciones_genero.index(st.session_state.match_genero),
    )

    if genero_elegido != st.session_state.match_genero:
        st.session_state.match_genero = genero_elegido
        st.session_state.match_deck = []
        st.session_state.match_pagina = 1
        st.rerun()

    # Si el mazo está vacío, trae más películas del género elegido
    if not st.session_state.match_deck:
        genero_id = mapa_generos.get(genero_elegido) if genero_elegido != "Todos" else None
        data = descubrir_tmdb(genero_id, st.session_state.match_pagina)
        candidatos = [
            r for r in data.get("results", [])
            if not existe_titulo(r.get("title", ""))
        ]
        st.session_state.match_deck = candidatos
        st.session_state.match_pagina += 1

    deck = st.session_state.match_deck

    if not deck:
        st.info("No hay más películas para mostrar con este filtro por ahora. Probá con otro género.")
    else:
        actual = deck[0]
        titulo = html.escape(actual.get("title", "Sin título"))
        rating = round(actual.get("vote_average", 0), 1)
        anio = (actual.get("release_date") or "")[:4]
        poster_path = actual.get("poster_path")
        backdrop_path = actual.get("backdrop_path") or poster_path
        imagen = (BACKDROP_BASE + backdrop_path) if backdrop_path else poster_url({"poster": None})

        st.markdown(
            compactar_html(f"""
            <div class="hero" style="height:420px;background-image:url('{imagen}')">
                <div class="hero-content">
                    <span class="hero-kicker">{len(deck)} en el mazo</span>
                    <h2>{titulo}</h2>
                    <p>{anio} · TMDb {rating}/10</p>
                </div>
            </div>
            """),
            unsafe_allow_html=True,
        )

        c_no, c_si = st.columns(2)
        with c_no:
            if st.button("✖ Paso", key="match_no", use_container_width=True):
                st.session_state.match_deck.pop(0)
                st.rerun()
        with c_si:
            if st.button("❤ Me interesa", key="match_si", type="primary", use_container_width=True):
                if not existe_titulo(actual.get("title", "")):
                    nueva = convertir_pelicula(actual)
                    nueva["para_despues"] = True
                    st.session_state.peliculas.append(nueva)
                else:
                    existente = encontrar_pelicula(actual.get("title", ""))
                    if existente:
                        existente["para_despues"] = True
                guardar_datos()
                st.session_state.match_deck.pop(0)
                st.rerun()

    guardadas = [p for p in st.session_state.peliculas if p.get("para_despues")]
    if guardadas:
        st.divider()
        st.subheader("Guardadas para ver después")
        render_grid(guardadas, "matchsaved")


# ============================================================
# MI COLECCIÓN
# ============================================================
elif menu == "Mi colección":
    calificadas = [
        p for p in st.session_state.peliculas
        if p.get("calificada")
    ]

    st.subheader("Mi colección")
    st.caption("Películas que ya calificaste o reseñaste.")

    if not calificadas:
        st.info("Todavía no calificaste ninguna película.")
    else:
        destacada = max(calificadas, key=lambda x: x.get("puntaje", 0))
        mostrar_hero(destacada, "Tu mejor puntuación")

        generos = sorted({
            p.get("genero", "Sin género").split(",")[0].strip()
            for p in calificadas
        })

        c1, c2 = st.columns(2)

        with c1:
            genero = st.selectbox("Género", ["Todos"] + generos, key="mc_genero")

        with c2:
            orden = st.selectbox(
                "Orden",
                ["Mi puntuación", "Alfabético"],
                key="mc_orden",
            )

        vista = [
            p for p in calificadas
            if genero == "Todos"
            or p.get("genero", "").split(",")[0].strip() == genero
        ]

        if orden == "Mi puntuación":
            vista.sort(key=lambda x: x.get("puntaje", 0), reverse=True)
        else:
            vista.sort(key=lambda x: x.get("titulo", "").lower())

        st.caption(f"{len(vista)} película(s)")
        render_grid(vista, "collection")


# ============================================================
# BUSCAR
# ============================================================
elif menu == "Buscar":
    st.subheader("Buscar películas")
    st.caption("Buscá directamente en TMDb, no solamente en tu colección.")

    q = st.text_input(
        "Título",
        placeholder="Escribí el nombre de una película...",
    )

    if q.strip():
        if q != st.session_state.busqueda_actual:
            st.session_state.busqueda_actual = q
            st.session_state.pagina_busqueda = 1

        data = buscar_tmdb(q, st.session_state.pagina_busqueda)
        resultados = data.get("results", [])
        total_pages = min(data.get("total_pages", 1), 500)

        if resultados:
            cards = [convertir_pelicula(r) for r in resultados]
            render_grid(cards, "search")

            st.divider()
            c1, c2 = st.columns(2)

            with c1:
                if st.session_state.pagina_busqueda > 1:
                    if st.button("Página anterior", use_container_width=True):
                        st.session_state.pagina_busqueda -= 1
                        st.rerun()

            with c2:
                if st.button(
                    "Siguiente página",
                    type="primary",
                    use_container_width=True,
                    disabled=st.session_state.pagina_busqueda >= total_pages,
                ):
                    st.session_state.pagina_busqueda += 1
                    st.rerun()
        else:
            st.warning("No se encontraron películas.")


# ============================================================
# ESTADÍSTICAS
# ============================================================
elif menu == "Estadísticas":
    peliculas = st.session_state.peliculas

    st.subheader("Estadísticas")

    if not peliculas:
        st.info("No hay películas cargadas.")
    else:
        calificadas = [
            p for p in peliculas if p.get("calificada")
        ]

        promedio = (
            sum(p.get("puntaje", 0) for p in calificadas) / len(calificadas)
            if calificadas else 0
        )

        total_recaudacion = sum(
            p.get("recaudacion", 0) for p in peliculas
        )

        mejor = (
            max(calificadas, key=lambda x: x.get("puntaje", 0))
            if calificadas else None
        )

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Películas", len(peliculas))
        c2.metric("Calificadas", len(calificadas))
        c3.metric("Promedio", f"{promedio:.1f}/10")
        c4.metric("Recaudación", f"${total_recaudacion:,.0f}")

        if mejor:
            st.divider()
            st.markdown(
                f"### Tu favorita actual: {html.escape(mejor.get('titulo',''))}"
            )
            st.caption(
                f"Puntuación {mejor.get('puntaje',0)}/10 · "
                f"TMDb {mejor.get('tmdb_rating',0)}/10"
            )

        st.divider()
        st.markdown("### Distribución de tus puntuaciones")

        distribucion = {i: 0 for i in range(1, 11)}
        for p in calificadas:
            valor = int(p.get("puntaje", 0))
            if 1 <= valor <= 10:
                distribucion[valor] += 1

        for nota, cantidad in distribucion.items():
            if cantidad:
                st.write(f"{nota}/10 — {cantidad} película(s)")


# ============================================================
# AGREGAR
# ============================================================
elif menu == "Agregar película":
    st.subheader("Agregar película")
    st.caption("Buscala en TMDb y agregala a tu catálogo con tu puntuación.")

    q = st.text_input(
        "Buscar",
        placeholder="Ej. Interstellar",
        key="add_search",
    )

    if q.strip():
        data = buscar_tmdb(q)
        resultados = data.get("results", [])

        if resultados:
            opciones = {
                f"{r.get('title','Sin título')} "
                f"({r.get('release_date','')[:4] or 's/f'})": r
                for r in resultados
            }

            elegido = st.selectbox("Resultados", list(opciones.keys()))
            r = opciones[elegido]
            detalle = detalle_tmdb(r["id"])
            pelicula = convertir_pelicula(r, detalle)

            col1, col2 = st.columns([1, 2], gap="large")

            with col1:
                st.image(poster_url(pelicula), use_container_width=True)

            with col2:
                st.markdown(f"## {pelicula['titulo']}")
                st.write(
                    f"**Género:** {pelicula['genero']}  \n"
                    f"**Duración:** {pelicula['duracion'] or '—'} min  \n"
                    f"**TMDb:** {pelicula['tmdb_rating']}/10"
                )

                if pelicula["descripcion"]:
                    st.write(pelicula["descripcion"])

                puntaje = st.slider(
                    "Tu puntuación",
                    1,
                    10,
                    5,
                    key="add_score",
                )

                comentario = st.text_area(
                    "Tu comentario",
                    placeholder="Opcional",
                    key="add_comment",
                )

                if st.button(
                    "Agregar a mi colección",
                    type="primary",
                    use_container_width=True,
                ):
                    if existe_titulo(pelicula["titulo"]):
                        st.warning("Esa película ya está en tu colección.")
                    else:
                        pelicula["puntaje"] = puntaje
                        pelicula["comentario"] = comentario
                        pelicula["calificada"] = True

                        st.session_state.peliculas.append(pelicula)
                        guardar_datos()

                        st.success(
                            f"{pelicula['titulo']} fue agregada correctamente."
                        )
                        st.rerun()
        else:
            st.warning("No se encontraron resultados.")
