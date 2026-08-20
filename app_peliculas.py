import streamlit as st
import requests

st.set_page_config(page_title="Gestión de Películas", page_icon="🎬", layout="wide")

# ----------------------------------------
# API de The Movie Database (TMDb) - gratis
# Sacá tu API key en: https://www.themoviedb.org/settings/api
# ----------------------------------------
TMDB_API_KEY = "PONE_ACA_TU_API_KEY"
TMDB_BASE = "https://api.themoviedb.org/3"
POSTER_BASE = "https://image.tmdb.org/t/p/w500"

# ----------------------------------------
# Estilos
# ----------------------------------------
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(180deg, #0e1117 0%, #14171f 100%);
    }
    h1, h2, h3 {
        font-family: 'Helvetica Neue', sans-serif;
    }
    .pelicula-card {
        background-color: #1c1f2b;
        border-radius: 14px;
        padding: 14px;
        margin-bottom: 16px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.35);
        transition: transform 0.15s ease;
    }
    .pelicula-card:hover {
        transform: translateY(-4px);
    }
    .puntaje-badge {
        display: inline-block;
        background-color: #e50914;
        color: white;
        border-radius: 20px;
        padding: 2px 12px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .genero-badge {
        display: inline-block;
        background-color: #2a2f42;
        color: #cfd3e0;
        border-radius: 20px;
        padding: 2px 10px;
        font-size: 0.8rem;
        margin-right: 6px;
    }
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


st.title("🎬 Sistema de Gestión de Películas")

menu = st.sidebar.radio(
    "Menú",
    [
        "Cargar película",
        "Mostrar películas",
        "Actualizar puntaje",
        "Ordenar películas",
        "Buscar por título",
        "Buscar por género",
        "Estadísticas",
    ],
)

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
                    }
                )
                st.success(f"'{titulo_m}' cargada correctamente")

# ----------------------------------------
# Mostrar películas (grilla de tarjetas)
# ----------------------------------------
elif menu == "Mostrar películas":
    st.subheader("Películas cargadas")

    peliculas = st.session_state.peliculas

    if not peliculas:
        st.info("No hay películas cargadas")
    else:
        columnas = st.columns(4)
        for i, p in enumerate(peliculas):
            with columnas[i % 4]:
                st.markdown('<div class="pelicula-card">', unsafe_allow_html=True)
                if p.get("poster"):
                    st.image(p["poster"], use_container_width=True)
                st.markdown(f"**{p['titulo']}**")
                st.markdown(f'<span class="genero-badge">{p["genero"]}</span>', unsafe_allow_html=True)
                st.markdown(f'<span class="puntaje-badge">⭐ {p["puntaje"]}/10</span>', unsafe_allow_html=True)
                st.caption(f"{p['duracion']} min · ${p['recaudacion']:,.0f}")
                st.markdown("</div>", unsafe_allow_html=True)

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