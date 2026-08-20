import streamlit as st
import requests

st.set_page_config(page_title="Gestión de Películas", page_icon="🎬", layout="wide")

# ----------------------------------------
# API de The Movie Database (TMDb) - gratis
# Sacá tu API key en: https://www.themoviedb.org/settings/api
# ----------------------------------------
TMDB_API_KEY = "8a5fe9643d4410984062cd935e4a8fa7"
TMDB_BASE = "https://api.themoviedb.org/3"
POSTER_BASE = "https://image.tmdb.org/t/p/w500"
BACKDROP_BASE = "https://image.tmdb.org/t/p/w1280"

# ----------------------------------------
# Estilos
# ----------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&family=Inter:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: radial-gradient(circle at 20% 0%, #1a1033 0%, #0b0c14 45%, #08090f 100%);
    }

    h1, h2, h3 {
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
    }

    /* Header tipo hero */
    .hero-header {
        background: linear-gradient(120deg, #e50914 0%, #7b2ff7 100%);
        border-radius: 20px;
        padding: 28px 32px;
        margin-bottom: 28px;
        box-shadow: 0 10px 30px rgba(123, 47, 247, 0.25);
    }
    .hero-header h1 {
        color: white;
        margin: 0;
        font-size: 2.1rem;
        letter-spacing: -0.5px;
    }
    .hero-header p {
        color: rgba(255,255,255,0.85);
        margin: 4px 0 0 0;
        font-size: 0.95rem;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #0f1018;
        border-right: 1px solid rgba(255,255,255,0.06);
    }
    section[data-testid="stSidebar"] .stRadio label {
        font-family: 'Poppins', sans-serif;
        font-size: 0.95rem;
    }

    /* Tarjetas de película */
    .pelicula-card {
        background: linear-gradient(160deg, #1c1f2e 0%, #15161f 100%);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 16px;
        padding: 14px;
        margin-bottom: 18px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.4);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .pelicula-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 14px 30px rgba(123, 47, 247, 0.25);
    }
    .pelicula-card img {
        border-radius: 10px;
    }

    .puntaje-badge {
        display: inline-block;
        background: linear-gradient(120deg, #e50914, #ff4d67);
        color: white;
        border-radius: 20px;
        padding: 3px 14px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .genero-badge {
        display: inline-block;
        background-color: rgba(123, 47, 247, 0.18);
        color: #cbb6ff;
        border: 1px solid rgba(123, 47, 247, 0.35);
        border-radius: 20px;
        padding: 3px 12px;
        font-size: 0.78rem;
        margin-right: 6px;
    }

    /* Botones */
    .stButton > button {
        background: linear-gradient(120deg, #e50914, #7b2ff7);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        padding: 8px 20px;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 18px rgba(123, 47, 247, 0.35);
        color: white;
    }

    /* Inputs, selects, sliders */
    div[data-baseweb="select"] > div, .stTextInput input, .stNumberInput input {
        background-color: #171923 !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
    }

    /* Métricas */
    div[data-testid="stMetric"] {
        background: #15161f;
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 14px;
        padding: 14px;
    }

    /* Banner destacado (estilo Netflix) */
    .featured-banner {
        position: relative;
        border-radius: 20px;
        overflow: hidden;
        height: 340px;
        margin-bottom: 32px;
        background-size: cover;
        background-position: center 20%;
        box-shadow: 0 14px 40px rgba(0,0,0,0.55);
    }
    .featured-banner::after {
        content: "";
        position: absolute;
        inset: 0;
        background: linear-gradient(0deg, #08090f 5%, rgba(8,9,15,0.35) 55%, rgba(8,9,15,0.15) 100%),
                    linear-gradient(90deg, rgba(8,9,15,0.85) 0%, rgba(8,9,15,0.1) 55%);
    }
    .featured-content {
        position: absolute;
        left: 32px;
        bottom: 26px;
        z-index: 2;
        max-width: 55%;
    }
    .featured-tag {
        display: inline-block;
        background: rgba(229, 9, 20, 0.9);
        color: white;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        padding: 3px 10px;
        border-radius: 6px;
        margin-bottom: 10px;
    }
    .featured-content h2 {
        color: white;
        font-size: 2.2rem;
        margin: 0 0 8px 0;
        text-shadow: 0 2px 12px rgba(0,0,0,0.6);
    }
    .featured-content p {
        color: rgba(255,255,255,0.85);
        font-size: 0.95rem;
        margin: 0;
    }

    /* Filas horizontales estilo Netflix */
    .fila-genero-titulo {
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        font-size: 1.15rem;
        color: #eee;
        margin: 6px 0 12px 2px;
    }
    .fila-scroll {
        display: flex;
        gap: 14px;
        overflow-x: auto;
        padding-bottom: 14px;
        margin-bottom: 22px;
        scrollbar-width: thin;
        scrollbar-color: #7b2ff7 #15161f;
    }
    .fila-scroll::-webkit-scrollbar {
        height: 8px;
    }
    .fila-scroll::-webkit-scrollbar-thumb {
        background: #7b2ff7;
        border-radius: 10px;
    }
    .fila-scroll::-webkit-scrollbar-track {
        background: #15161f;
    }
    .mini-card {
        flex: 0 0 auto;
        width: 150px;
        border-radius: 12px;
        overflow: hidden;
        background: #15161f;
        border: 1px solid rgba(255,255,255,0.06);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        cursor: pointer;
    }
    .mini-card:hover {
        transform: translateY(-6px) scale(1.04);
        box-shadow: 0 12px 26px rgba(123, 47, 247, 0.35);
        z-index: 3;
    }
    .mini-card img {
        width: 150px;
        height: 220px;
        object-fit: cover;
        display: block;
    }
    .mini-card .mini-info {
        padding: 8px 10px;
    }
    .mini-card .mini-titulo {
        font-size: 0.8rem;
        font-weight: 600;
        color: #eee;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .mini-card .mini-puntaje {
        font-size: 0.72rem;
        color: #ff4d67;
        font-weight: 700;
    }

    /* Ocultar la barra de Streamlit Cloud (ícono de GitHub, menú "..."), y el footer */
    header[data-testid="stHeader"] {
        background: transparent;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    div[data-testid="stToolbar"] {visibility: hidden;}
    div[data-testid="stDecoration"] {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

if "peliculas" not in st.session_state:
    st.session_state.peliculas = []  # {"titulo","genero","duracion","recaudacion","puntaje","poster"}


def existe_titulo(titulo, ignorar_index=None):
    for i, p in enumerate(st.session_state.peliculas):
        if i == ignorar_index:
            continue
        if p["titulo"].lower() == titulo.lower():
            return True
    return False


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


st.markdown(
    """
    <div class="hero-header">
        <h1>🎬 CineVega</h1>
        <p>Tu sistema personal de gestión de películas</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown("### 📽️ CineVega")

opcion_menu = st.sidebar.radio(
    "Menú",
    [
        "➕ Cargar película",
        "🎞️ Mostrar películas",
        "⭐ Actualizar puntaje",
        "🔤 Ordenar películas",
        "🔍 Buscar por título",
        "🎭 Buscar por género",
        "📊 Estadísticas",
    ],
)
menu = opcion_menu.split(" ", 1)[1]

# ----------------------------------------
# Cargar película (con autocompletado desde TMDb)
# ----------------------------------------
if menu == "Cargar película":
    st.subheader("Cargar película")

    if TMDB_API_KEY == "PONE_ACA_TU_API_KEY":
        st.warning(
            "Para que la búsqueda y el poster se carguen solos, "
            "necesitás una API key gratis de TMDb (themoviedb.org/settings/api) "
            "y pegarla en la variable TMDB_API_KEY del código."
        )

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
            if poster_url:
                st.image(poster_url, use_container_width=True)
            else:
                st.info("Sin poster disponible")

        with col_info:
            titulo = seleccionada["title"]
            genero = ", ".join(g["name"] for g in detalle["genres"]) if detalle and detalle.get("genres") else "Sin género"
            duracion = detalle.get("runtime") if detalle else None
            recaudacion = detalle.get("revenue") if detalle else 0

            st.write(f"**Título:** {titulo}")
            st.write(f"**Género:** {genero}")
            st.write(f"**Duración:** {duracion if duracion else '—'} minutos")
            st.write(f"**Recaudación (TMDb):** ${recaudacion:,.0f}" if recaudacion else "**Recaudación (TMDb):** sin datos")

            puntaje = st.slider("Tu puntaje", 1, 10, 5)

            if st.button("Cargar esta película", type="primary"):
                if existe_titulo(titulo):
                    st.error("La película ya existe")
                else:
                    st.session_state.peliculas.append(
                        {
                            "titulo": titulo,
                            "genero": genero,
                            "duracion": duracion if duracion else 0,
                            "recaudacion": recaudacion if recaudacion else 0,
                            "puntaje": puntaje,
                            "poster": poster_url,
                            "backdrop": backdrop_url,
                        }
                    )
                    st.success(f"'{titulo}' cargada correctamente")

    st.divider()
    with st.expander("¿No la encontrás? Cargala a mano"):
        with st.form("form_manual", clear_on_submit=True):
            titulo_m = st.text_input("Título")
            genero_m = st.text_input("Género")
            duracion_m = st.number_input("Duración (minutos)", min_value=1, step=1)
            recaudacion_m = st.number_input("Recaudación (USD)", min_value=0.0, step=1000.0, format="%.2f")
            puntaje_m = st.slider("Puntaje", 1, 10, 5, key="puntaje_manual")
            enviar_m = st.form_submit_button("Cargar")

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
                        "puntaje": puntaje_m,
                        "poster": None,
                        "backdrop": None,
                    }
                )
                st.success(f"'{titulo_m}' cargada correctamente")

# ----------------------------------------
# Mostrar películas (estilo Netflix: banner + filas por género)
# ----------------------------------------
elif menu == "Mostrar películas":
    peliculas = st.session_state.peliculas

    if not peliculas:
        st.info("No hay películas cargadas")
    else:
        # --- Banner destacado: la de mayor puntaje ---
        destacada = max(peliculas, key=lambda p: p["puntaje"])
        imagen_banner = destacada.get("backdrop") or destacada.get("poster")

        if imagen_banner:
            st.markdown(
                f"""
                <div class="featured-banner" style="background-image: url('{imagen_banner}');">
                    <div class="featured-content">
                        <span class="featured-tag">⭐ Tu mejor puntuada</span>
                        <h2>{destacada['titulo']}</h2>
                        <p>{destacada['genero']} · {destacada['duracion']} min · Puntaje {destacada['puntaje']}/10</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # --- Agrupar por género (primer género de cada película) ---
        generos_orden = []
        peliculas_por_genero = {}
        for p in peliculas:
            genero_principal = p["genero"].split(",")[0].strip()
            if genero_principal not in peliculas_por_genero:
                peliculas_por_genero[genero_principal] = []
                generos_orden.append(genero_principal)
            peliculas_por_genero[genero_principal].append(p)

        for genero in generos_orden:
            st.markdown(f'<div class="fila-genero-titulo">🎬 {genero}</div>', unsafe_allow_html=True)

            tarjetas_html = ""
            for p in peliculas_por_genero[genero]:
                poster = p.get("poster") or "https://via.placeholder.com/150x220/15161f/666666?text=Sin+poster"
                tarjetas_html += f"""
                <div class="mini-card">
                    <img src="{poster}">
                    <div class="mini-info">
                        <div class="mini-titulo">{p['titulo']}</div>
                        <div class="mini-puntaje">⭐ {p['puntaje']}/10</div>
                    </div>
                </div>
                """

            st.markdown(f'<div class="fila-scroll">{tarjetas_html}</div>', unsafe_allow_html=True)

# ----------------------------------------
# Actualizar puntaje
# ----------------------------------------
elif menu == "Actualizar puntaje":
    st.subheader("Actualizar puntaje")

    if not st.session_state.peliculas:
        st.info("No hay películas cargadas")
    else:
        titulos = [p["titulo"] for p in st.session_state.peliculas]
        elegido = st.selectbox("Película", titulos)
        nuevo = st.slider("Nuevo puntaje", 1, 10, 5)

        if st.button("Actualizar"):
            for p in st.session_state.peliculas:
                if p["titulo"] == elegido:
                    p["puntaje"] = nuevo
            st.success("Puntaje actualizado correctamente")

# ----------------------------------------
# Ordenar películas
# ----------------------------------------
elif menu == "Ordenar películas":
    st.subheader("Ordenar alfabéticamente")

    if not st.session_state.peliculas:
        st.info("No hay películas cargadas")
    else:
        if st.button("Ordenar"):
            st.session_state.peliculas.sort(key=lambda p: p["titulo"].lower())
            st.success("Películas ordenadas correctamente")

        columnas = st.columns(4)
        for i, p in enumerate(st.session_state.peliculas):
            with columnas[i % 4]:
                st.markdown('<div class="pelicula-card">', unsafe_allow_html=True)
                if p.get("poster"):
                    st.image(p["poster"], use_container_width=True)
                st.markdown(f"**{p['titulo']}**")
                st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------------
# Buscar por título
# ----------------------------------------
elif menu == "Buscar por título":
    st.subheader("Buscar película por título")

    titulo = st.text_input("Título a buscar")

    if titulo:
        encontrada = next(
            (p for p in st.session_state.peliculas if p["titulo"].lower() == titulo.lower()),
            None,
        )
        if encontrada:
            col_img, col_info = st.columns([1, 2])
            with col_img:
                if encontrada.get("poster"):
                    st.image(encontrada["poster"], use_container_width=True)
            with col_info:
                st.write(f"**Título:** {encontrada['titulo']}")
                st.write(f"**Género:** {encontrada['genero']}")
                st.write(f"**Duración:** {encontrada['duracion']} minutos")
                st.write(f"**Recaudación:** ${encontrada['recaudacion']:,.0f}")
                st.write(f"**Puntaje:** {encontrada['puntaje']}/10")
        else:
            st.warning("La película no existe")

# ----------------------------------------
# Buscar por género
# ----------------------------------------
elif menu == "Buscar por género":
    st.subheader("Buscar películas por género")

    genero = st.text_input("Género a buscar")

    if genero:
        resultado = [p for p in st.session_state.peliculas if genero.lower() in p["genero"].lower()]
        if resultado:
            columnas = st.columns(4)
            for i, p in enumerate(resultado):
                with columnas[i % 4]:
                    st.markdown('<div class="pelicula-card">', unsafe_allow_html=True)
                    if p.get("poster"):
                        st.image(p["poster"], use_container_width=True)
                    st.markdown(f"**{p['titulo']}**")
                    st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.warning("No hay películas de ese género")

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
        col2.metric("Promedio de puntajes", round(sum(puntajes) / len(puntajes), 2))
        col3.metric("Recaudación total", f"${sum(recaudaciones):,.0f}")

        st.write("**Mayor puntaje:**", mayor["titulo"], f"({mayor['puntaje']})")
        st.write("**Menor puntaje:**", menor["titulo"], f"({menor['puntaje']})")
        st.write("**Más taquillera:**", mas_taquillera["titulo"], f"(${mas_taquillera['recaudacion']:,.0f})")
