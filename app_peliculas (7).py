import streamlit as st
import requests

st.set_page_config(page_title="CineVega", page_icon="🎬", layout="wide")

# ----------------------------------------
# API de The Movie Database (TMDb) - gratis
# Sacá tu API key en: https://www.themoviedb.org/settings/api
# ----------------------------------------
TMDB_API_KEY = "8a5fe9643d4410984062cd935e4a8fa7"
TMDB_BASE = "https://api.themoviedb.org/3"
POSTER_BASE = "https://image.tmdb.org/t/p/w500"
BACKDROP_BASE = "https://image.tmdb.org/t/p/w1280"
PLACEHOLDER = "https://via.placeholder.com/300x445/15161f/666666?text=Sin+poster"


def compactar_html(html):
    """Saca la sangría de cada línea para que Streamlit/Markdown no la confunda con un bloque de código."""
    return "\n".join(linea.strip() for linea in html.strip().splitlines())

# ----------------------------------------
# Estilos
# ----------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&family=Inter:wght@400;500&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background: radial-gradient(circle at 20% 0%, #1a1033 0%, #0b0c14 45%, #08090f 100%); }
    h1, h2, h3 { font-family: 'Poppins', sans-serif; font-weight: 700; }

    .hero-header {
        background: linear-gradient(120deg, #e50914 0%, #7b2ff7 100%);
        border-radius: 20px; padding: 24px 32px; margin-bottom: 26px;
        box-shadow: 0 10px 30px rgba(123, 47, 247, 0.25);
    }
    .hero-header h1 { color: white; margin: 0; font-size: 2rem; letter-spacing: -0.5px; }
    .hero-header p { color: rgba(255,255,255,0.85); margin: 4px 0 0 0; font-size: 0.92rem; }

    section[data-testid="stSidebar"] { background: #0f1018; border-right: 1px solid rgba(255,255,255,0.06); }
    section[data-testid="stSidebar"] .stRadio label { font-family: 'Poppins', sans-serif; font-size: 0.95rem; }

    .featured-banner {
        position: relative; border-radius: 20px; overflow: hidden; height: 320px;
        margin-bottom: 30px; background-size: cover; background-position: center 20%;
        box-shadow: 0 14px 40px rgba(0,0,0,0.55);
    }
    .featured-banner::after {
        content: ""; position: absolute; inset: 0;
        background: linear-gradient(0deg, #08090f 5%, rgba(8,9,15,0.35) 55%, rgba(8,9,15,0.15) 100%),
                    linear-gradient(90deg, rgba(8,9,15,0.85) 0%, rgba(8,9,15,0.1) 55%);
    }
    .featured-content { position: absolute; left: 30px; bottom: 24px; z-index: 2; max-width: 55%; }
    .featured-tag {
        display: inline-block; background: rgba(229, 9, 20, 0.9); color: white;
        font-size: 0.7rem; font-weight: 700; letter-spacing: 1px; text-transform: uppercase;
        padding: 3px 10px; border-radius: 6px; margin-bottom: 8px;
    }
    .featured-content h2 { color: white; font-size: 2rem; margin: 0 0 6px 0; text-shadow: 0 2px 12px rgba(0,0,0,0.6); }
    .featured-content p { color: rgba(255,255,255,0.85); font-size: 0.9rem; margin: 0; }

    .fila-genero-titulo { font-family: 'Poppins', sans-serif; font-weight: 600; font-size: 1.1rem; color: #eee; margin: 4px 0 10px 2px; }
    .fila-scroll {
        display: flex; gap: 14px; overflow-x: auto; padding-bottom: 12px; margin-bottom: 20px;
        scrollbar-width: thin; scrollbar-color: #7b2ff7 #15161f;
    }
    .fila-scroll::-webkit-scrollbar { height: 8px; }
    .fila-scroll::-webkit-scrollbar-thumb { background: #7b2ff7; border-radius: 10px; }
    .fila-scroll::-webkit-scrollbar-track { background: #15161f; }
    .mini-card {
        flex: 0 0 auto; width: 140px; border-radius: 12px; overflow: hidden;
        background: #15161f; border: 1px solid rgba(255,255,255,0.06);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .mini-card:hover { transform: translateY(-5px) scale(1.03); box-shadow: 0 12px 26px rgba(123, 47, 247, 0.35); }
    .mini-card img { width: 140px; height: 205px; object-fit: cover; display: block; }
    .mini-card .mini-info { padding: 7px 9px; }
    .mini-card .mini-titulo { font-size: 0.78rem; font-weight: 600; color: #eee; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .mini-card .mini-puntaje { font-size: 0.7rem; color: #ff4d67; font-weight: 700; }

    .ficha-card {
        background: linear-gradient(160deg, #1c1f2e 0%, #15161f 100%);
        border: 1px solid rgba(255,255,255,0.06); border-radius: 16px; padding: 18px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.4); margin-bottom: 18px;
    }
    .genero-badge {
        display: inline-block; background-color: rgba(123, 47, 247, 0.18); color: #cbb6ff;
        border: 1px solid rgba(123, 47, 247, 0.35); border-radius: 20px; padding: 3px 12px;
        font-size: 0.78rem; margin-right: 6px;
    }
    .stat-chip {
        display: inline-block; background: #171923; border: 1px solid rgba(255,255,255,0.08);
        border-radius: 10px; padding: 8px 16px; margin-right: 10px; margin-bottom: 8px;
    }
    .stat-chip .stat-label { font-size: 0.72rem; color: #9a9fb0; display: block; }
    .stat-chip .stat-value { font-size: 1.05rem; font-weight: 700; color: #eee; }

    .stButton > button {
        background: linear-gradient(120deg, #e50914, #7b2ff7); color: white; border: none;
        border-radius: 10px; font-weight: 600; padding: 8px 20px;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .stButton > button:hover { transform: translateY(-2px); box-shadow: 0 8px 18px rgba(123, 47, 247, 0.35); color: white; }

    div[data-baseweb="select"] > div, .stTextInput input, .stNumberInput input, .stTextArea textarea {
        background-color: #171923 !important; border-radius: 10px !important; border: 1px solid rgba(255,255,255,0.08) !important;
    }
    div[data-testid="stMetric"] { background: #15161f; border: 1px solid rgba(255,255,255,0.06); border-radius: 14px; padding: 14px; }

    header[data-testid="stHeader"] { background: transparent; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    div[data-testid="stToolbar"] {visibility: hidden;}
    div[data-testid="stDecoration"] {visibility: hidden;}

    /* Flechita para abrir/cerrar la sidebar: siempre visible y con contraste
       (varios selectores porque el nombre interno cambia según la versión de Streamlit) */
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="collapsedControl"],
    [data-testid="stSidebarCollapseButton"],
    [data-testid="stSidebarContent"] button[kind="header"],
    section[data-testid="stSidebar"] button,
    header[data-testid="stHeader"] button {
        visibility: visible !important;
        display: flex !important;
        opacity: 1 !important;
        background: #7b2ff7 !important;
        border-radius: 8px !important;
        padding: 4px !important;
        position: relative !important;
        z-index: 999999 !important;
    }
    [data-testid="stSidebarCollapsedControl"] svg,
    [data-testid="collapsedControl"] svg,
    [data-testid="stSidebarCollapseButton"] svg,
    header[data-testid="stHeader"] svg,
    section[data-testid="stSidebar"] svg {
        fill: white !important;
        stroke: white !important;
        opacity: 1 !important;
    }
    header[data-testid="stHeader"] {
        visibility: visible !important;
        height: auto !important;
        z-index: 999998 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def existe_titulo(titulo, ignorar_index=None):
    for i, p in enumerate(st.session_state.peliculas):
        if i == ignorar_index:
            continue
        if p["titulo"].lower() == titulo.lower():
            return True
    return False


def encontrar_pelicula(titulo):
    for p in st.session_state.peliculas:
        if p["titulo"] == titulo:
            return p
    return None


def buscar_en_tmdb(query):
    try:
        resp = requests.get(
            f"{TMDB_BASE}/search/movie",
            params={"api_key": TMDB_API_KEY, "query": query, "language": "es-ES"},
            timeout=6,
        )
        resp.raise_for_status()
        return resp.json().get("results", [])[:8]
    except Exception:
        return []


def detalle_en_tmdb(movie_id):
    try:
        resp = requests.get(
            f"{TMDB_BASE}/movie/{movie_id}",
            params={"api_key": TMDB_API_KEY, "language": "es-ES"},
            timeout=6,
        )
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return None


def populares_en_tmdb(pagina=1):
    try:
        resp = requests.get(
            f"{TMDB_BASE}/movie/popular",
            params={"api_key": TMDB_API_KEY, "language": "es-ES", "page": pagina},
            timeout=6,
        )
        resp.raise_for_status()
        return resp.json().get("results", [])
    except Exception:
        return []


def pelicula_desde_resultado_tmdb(resultado, detalle=None):
    """Arma el diccionario de película a partir de un resultado de búsqueda/populares de TMDb."""
    if detalle is None:
        detalle = detalle_en_tmdb(resultado["id"])

    poster_path = resultado.get("poster_path")
    poster_url = POSTER_BASE + poster_path if poster_path else None
    backdrop_path = (detalle.get("backdrop_path") if detalle else None) or resultado.get("backdrop_path")
    backdrop_url = BACKDROP_BASE + backdrop_path if backdrop_path else poster_url

    genero = (
        ", ".join(g["name"] for g in detalle["genres"])
        if detalle and detalle.get("genres")
        else "Sin género"
    )

    return {
        "titulo": resultado["title"],
        "genero": genero,
        "duracion": (detalle.get("runtime") if detalle else 0) or 0,
        "recaudacion": (detalle.get("revenue") if detalle else 0) or 0,
        "poster": poster_url,
        "backdrop": backdrop_url,
        "tmdb_rating": round(resultado.get("vote_average", 0), 1),
        "tmdb_votes": resultado.get("vote_count", 0),
        "puntaje": 5,
        "comentario": "",
        "calificada": False,
    }


# ----------------------------------------
# Estado inicial: la colección arranca con populares de TMDb
# ----------------------------------------
if "peliculas" not in st.session_state:
    st.session_state.peliculas = []
    st.session_state.pagina_populares = 1
    # cada item: titulo, genero, duracion, recaudacion, poster, backdrop,
    #            tmdb_rating, tmdb_votes, puntaje (tu puntaje), comentario (tu reseña)

    if TMDB_API_KEY != "PONE_ACA_TU_API_KEY":
        with st.spinner("Cargando catálogo inicial de películas populares..."):
            for resultado in populares_en_tmdb(pagina=1):
                if not existe_titulo(resultado["title"]):
                    st.session_state.peliculas.append(pelicula_desde_resultado_tmdb(resultado))

if "pelicula_activa" not in st.session_state:
    st.session_state.pelicula_activa = None


def render_ficha(p):
    if st.button("← Volver"):
        st.session_state.pelicula_activa = None
        st.rerun()

    imagen_banner = p.get("backdrop") or p.get("poster")
    if imagen_banner:
        st.markdown(
            compactar_html(f"""
            <div class="featured-banner" style="background-image: url('{imagen_banner}'); height: 240px;">
                <div class="featured-content">
                    <h2>{p['titulo']}</h2>
                    <p>{p['genero']} · {p['duracion']} min</p>
                </div>
            </div>
            """),
            unsafe_allow_html=True,
        )

    col_img, col_info = st.columns([1, 2])
    with col_img:
        st.image(p.get("poster") or PLACEHOLDER, use_container_width=True)

    with col_info:
        st.markdown('<div class="ficha-card">', unsafe_allow_html=True)

        valor_tu_puntaje = f"⭐ {p['puntaje']}/10" if p.get("calificada") else "Sin calificar todavía"
        chips = compactar_html(f"""
        <span class="stat-chip"><span class="stat-label">Recaudación</span>
            <span class="stat-value">${p['recaudacion']:,.0f}</span></span>
        <span class="stat-chip"><span class="stat-label">Puntaje TMDb (comunidad)</span>
            <span class="stat-value">⭐ {p['tmdb_rating']}/10 ({p['tmdb_votes']} votos)</span></span>
        <span class="stat-chip"><span class="stat-label">Tu puntaje</span>
            <span class="stat-value">{valor_tu_puntaje}</span></span>
        """)
        st.markdown(chips, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("#### 📝 Tu reseña")
        with st.form(f"form_resena_{p['titulo']}"):
            nuevo_puntaje = st.slider("Tu puntaje", 1, 10, p["puntaje"])
            nuevo_comentario = st.text_area(
                "Tu comentario",
                value=p.get("comentario", ""),
                placeholder="¿Qué te pareció la película?",
                height=110,
            )
            guardar = st.form_submit_button("Guardar reseña")

        if guardar:
            p["puntaje"] = nuevo_puntaje
            p["comentario"] = nuevo_comentario
            p["calificada"] = True
            st.success("Reseña guardada")
            st.rerun()

        if p.get("comentario"):
            st.caption("Tu comentario actual:")
            st.write(p["comentario"])


def render_fila(titulo_fila, lista, key_prefix):
    st.markdown(f'<div class="fila-genero-titulo">🎬 {titulo_fila}</div>', unsafe_allow_html=True)
    tarjetas_html = ""
    for p in lista:
        poster = p.get("poster") or PLACEHOLDER
        rating_mostrado = p["tmdb_rating"] if p.get("tmdb_rating") else "—"
        tarjetas_html += compactar_html(f"""
        <div class="mini-card">
            <img src="{poster}">
            <div class="mini-info">
                <div class="mini-titulo">{p['titulo']}</div>
                <div class="mini-puntaje">🌐 {rating_mostrado}/10</div>
            </div>
        </div>
        """)
    st.markdown(f'<div class="fila-scroll">{tarjetas_html}</div>', unsafe_allow_html=True)

    titulos = [p["titulo"] for p in lista]
    elegido = st.selectbox(
        "Ver ficha de:", ["—"] + titulos, key=f"select_{key_prefix}_{titulo_fila}"
    )
    if elegido != "—":
        st.session_state.pelicula_activa = elegido
        st.rerun()


# ----------------------------------------
# Header + menú
# ----------------------------------------
st.markdown(
    compactar_html("""
    <div class="hero-header">
        <h1>🎬 CineVega</h1>
        <p>Tu colección personal de películas</p>
    </div>
    """),
    unsafe_allow_html=True,
)

st.sidebar.markdown("### 📽️ CineVega")
opcion_menu = st.sidebar.radio(
    "Menú",
    ["➕ Agregar película", "🎬 Mi colección", "🔍 Buscar", "📊 Estadísticas"],
)
menu = opcion_menu.split(" ", 1)[1]

pelicula_activa = encontrar_pelicula(st.session_state.pelicula_activa) if st.session_state.pelicula_activa else None

# ----------------------------------------
# Si hay una película activa, mostramos su ficha SIEMPRE, sin importar el menú
# ----------------------------------------
if pelicula_activa:
    render_ficha(pelicula_activa)

# ----------------------------------------
# Agregar película
# ----------------------------------------
elif menu == "Agregar película":
    st.subheader("Agregar película")

    query = st.text_input("Buscá la película por nombre")
    resultados = buscar_en_tmdb(query) if query.strip() else []

    seleccionada = None
    if resultados:
        opciones = {
            f"{r['title']} ({r['release_date'][:4] if r.get('release_date') else 's/f'})": r
            for r in resultados
        }
        elegido = st.selectbox("Resultados encontrados", list(opciones.keys()))
        seleccionada = opciones[elegido]

    if seleccionada:
        detalle = detalle_en_tmdb(seleccionada["id"])

        col_img, col_info = st.columns([1, 2])
        poster_path = seleccionada.get("poster_path")
        poster_url = POSTER_BASE + poster_path if poster_path else None
        backdrop_path = detalle.get("backdrop_path") if detalle else None
        backdrop_url = BACKDROP_BASE + backdrop_path if backdrop_path else poster_url

        with col_img:
            st.image(poster_url or PLACEHOLDER, use_container_width=True)

        with col_info:
            titulo = seleccionada["title"]
            genero = ", ".join(g["name"] for g in detalle["genres"]) if detalle and detalle.get("genres") else "Sin género"
            duracion = detalle.get("runtime") if detalle else 0
            recaudacion = detalle.get("revenue") if detalle else 0
            tmdb_rating = round(detalle.get("vote_average", 0), 1) if detalle else 0
            tmdb_votes = detalle.get("vote_count", 0) if detalle else 0

            st.write(f"**Título:** {titulo}")
            st.write(f"**Género:** {genero}")
            st.write(f"**Duración:** {duracion if duracion else '—'} minutos")
            st.write(f"**Recaudación (TMDb):** ${recaudacion:,.0f}" if recaudacion else "**Recaudación:** sin datos")
            st.write(f"**Puntaje comunidad TMDb:** ⭐ {tmdb_rating}/10 ({tmdb_votes} votos)")

            puntaje = st.slider("Tu puntaje", 1, 10, 5)
            comentario = st.text_area("Tu comentario (opcional, lo podés editar después)", height=90)

            if st.button("Agregar a mi colección", type="primary"):
                if existe_titulo(titulo):
                    st.error("Ya está en tu colección — entrá a 'Mi colección' para editar tu reseña")
                else:
                    st.session_state.peliculas.append(
                        {
                            "titulo": titulo,
                            "genero": genero,
                            "duracion": duracion or 0,
                            "recaudacion": recaudacion or 0,
                            "poster": poster_url,
                            "backdrop": backdrop_url,
                            "tmdb_rating": tmdb_rating,
                            "tmdb_votes": tmdb_votes,
                            "puntaje": puntaje,
                            "comentario": comentario,
                            "calificada": True,
                        }
                    )
                    st.success(f"'{titulo}' agregada a tu colección")

    st.divider()
    with st.expander("¿No la encontrás? Cargala a mano"):
        with st.form("form_manual", clear_on_submit=True):
            titulo_m = st.text_input("Título")
            genero_m = st.text_input("Género")
            duracion_m = st.number_input("Duración (minutos)", min_value=1, step=1)
            recaudacion_m = st.number_input("Recaudación (USD)", min_value=0.0, step=1000.0, format="%.2f")
            puntaje_m = st.slider("Tu puntaje", 1, 10, 5, key="puntaje_manual")
            comentario_m = st.text_area("Tu comentario (opcional)", height=90)
            enviar_m = st.form_submit_button("Agregar")

        if enviar_m:
            if titulo_m.strip() == "":
                st.error("El título no puede estar vacío")
            elif genero_m.strip() == "":
                st.error("El género no puede estar vacío")
            elif existe_titulo(titulo_m):
                st.error("La película ya existe")
            else:
                st.session_state.peliculas.append(
                    {
                        "titulo": titulo_m,
                        "genero": genero_m,
                        "duracion": duracion_m,
                        "recaudacion": recaudacion_m,
                        "poster": None,
                        "backdrop": None,
                        "tmdb_rating": 0,
                        "tmdb_votes": 0,
                        "puntaje": puntaje_m,
                        "comentario": comentario_m,
                        "calificada": True,
                    }
                )
                st.success(f"'{titulo_m}' agregada a tu colección")

# ----------------------------------------
# Mi colección (banner + filas por género)
# ----------------------------------------
elif menu == "Mi colección":
    peliculas = st.session_state.peliculas

    if not peliculas:
        st.info("Todavía no agregaste ninguna película")
    else:
        orden_alfabetico = st.checkbox("Ordenar géneros alfabéticamente")

        calificadas = [p for p in peliculas if p.get("calificada")]
        if calificadas:
            destacada = max(calificadas, key=lambda p: p["puntaje"])
            etiqueta_tag = "⭐ Tu mejor puntuada"
            etiqueta_detalle = f"Tu puntaje {destacada['puntaje']}/10"
        else:
            destacada = max(peliculas, key=lambda p: p["tmdb_rating"])
            etiqueta_tag = "🌐 Mejor valorada por la comunidad"
            etiqueta_detalle = f"Puntaje TMDb {destacada['tmdb_rating']}/10"

        imagen_banner = destacada.get("backdrop") or destacada.get("poster")
        if imagen_banner:
            st.markdown(
                compactar_html(f"""
                <div class="featured-banner" style="background-image: url('{imagen_banner}');">
                    <div class="featured-content">
                        <span class="featured-tag">{etiqueta_tag}</span>
                        <h2>{destacada['titulo']}</h2>
                        <p>{destacada['genero']} · {destacada['duracion']} min · {etiqueta_detalle}</p>
                    </div>
                </div>
                """),
                unsafe_allow_html=True,
            )

        generos_orden = []
        peliculas_por_genero = {}
        for p in peliculas:
            genero_principal = p["genero"].split(",")[0].strip()
            if genero_principal not in peliculas_por_genero:
                peliculas_por_genero[genero_principal] = []
                generos_orden.append(genero_principal)
            peliculas_por_genero[genero_principal].append(p)

        if orden_alfabetico:
            generos_orden.sort()

        for genero in generos_orden:
            render_fila(genero, peliculas_por_genero[genero], key_prefix="col")

        st.divider()
        if st.button("➕ Cargar más películas populares"):
            with st.spinner("Trayendo más películas..."):
                st.session_state.pagina_populares += 1
                nuevas = populares_en_tmdb(pagina=st.session_state.pagina_populares)
                agregadas = 0
                for resultado in nuevas:
                    if not existe_titulo(resultado["title"]):
                        st.session_state.peliculas.append(pelicula_desde_resultado_tmdb(resultado))
                        agregadas += 1
            st.success(f"Se agregaron {agregadas} películas nuevas")
            st.rerun()

# ----------------------------------------
# Buscar (en toda la base de TMDb, no solo en tu colección)
# ----------------------------------------
elif menu == "Buscar":
    st.subheader("🔍 Buscar cualquier película")
    st.caption("Busca en todo el catálogo de TMDb, no solo entre las que ya agregaste")

    texto = st.text_input("Nombre de la película")

    if texto.strip():
        resultados = buscar_en_tmdb(texto)

        if not resultados:
            st.warning("No se encontraron películas")
        else:
            tarjetas_html = ""
            for r in resultados:
                poster = POSTER_BASE + r["poster_path"] if r.get("poster_path") else PLACEHOLDER
                anio = r["release_date"][:4] if r.get("release_date") else "s/f"
                tarjetas_html += compactar_html(f"""
                <div class="mini-card">
                    <img src="{poster}">
                    <div class="mini-info">
                        <div class="mini-titulo">{r['title']}</div>
                        <div class="mini-puntaje">📅 {anio}</div>
                    </div>
                </div>
                """)
            st.markdown(f'<div class="fila-scroll">{tarjetas_html}</div>', unsafe_allow_html=True)

            opciones = {
                f"{r['title']} ({r['release_date'][:4] if r.get('release_date') else 's/f'})": r
                for r in resultados
            }
            elegido = st.selectbox("Ver ficha de:", ["—"] + list(opciones.keys()))

            if elegido != "—":
                resultado = opciones[elegido]
                if not existe_titulo(resultado["title"]):
                    with st.spinner("Cargando datos de la película..."):
                        nueva = pelicula_desde_resultado_tmdb(resultado)
                        st.session_state.peliculas.append(nueva)
                st.session_state.pelicula_activa = resultado["title"]
                st.rerun()

# ----------------------------------------
# Estadísticas
# ----------------------------------------
elif menu == "Estadísticas":
    st.subheader("📊 Estadísticas")

    peliculas = st.session_state.peliculas

    if not peliculas:
        st.info("No hay películas cargadas")
    else:
        puntajes = [p["puntaje"] for p in peliculas]
        recaudaciones = [p["recaudacion"] for p in peliculas]

        mayor = max(peliculas, key=lambda p: p["puntaje"])
        menor = min(peliculas, key=lambda p: p["puntaje"])
        mas_taquillera = max(peliculas, key=lambda p: p["recaudacion"])

        col1, col2, col3 = st.columns(3)
        col1.metric("Cantidad de películas", len(peliculas))
        col2.metric("Promedio de tu puntaje", round(sum(puntajes) / len(puntajes), 2))
        col3.metric("Recaudación total", f"${sum(recaudaciones):,.0f}")

        st.write("**Mejor puntuada por vos:**", mayor["titulo"], f"({mayor['puntaje']})")
        st.write("**Peor puntuada por vos:**", menor["titulo"], f"({menor['puntaje']})")
        st.write("**Más taquillera:**", mas_taquillera["titulo"], f"(${mas_taquillera['recaudacion']:,.0f})")
