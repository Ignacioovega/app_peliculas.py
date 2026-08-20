import streamlit as st

st.set_page_config(page_title="Gestión de Películas", page_icon="🎬", layout="centered")

# ----------------------------------------
# Estado (reemplaza a las listas globales del programa original)
# ----------------------------------------
if "peliculas" not in st.session_state:
    st.session_state.peliculas = []  # cada item: {"titulo","genero","duracion","recaudacion","puntaje"}


def existe_titulo(titulo, ignorar_index=None):
    for i, p in enumerate(st.session_state.peliculas):
        if i == ignorar_index:
            continue
        if p["titulo"].lower() == titulo.lower():
            return True
    return False


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
        "Eliminar película",
        "Estadísticas",
    ],
)

# ----------------------------------------
# Cargar película
# ----------------------------------------
if menu == "Cargar película":
    st.subheader("Cargar película")

    with st.form("form_cargar", clear_on_submit=True):
        titulo = st.text_input("Título")
        genero = st.text_input("Género")
        duracion = st.number_input("Duración (minutos)", min_value=1, step=1)
        recaudacion = st.number_input("Recaudación (USD)", min_value=0.0, step=1000.0, format="%.2f")
        puntaje = st.slider("Puntaje", 1, 10, 5)
        enviar = st.form_submit_button("Cargar")

    if enviar:
        if titulo.strip() == "":
            st.error("El título no puede estar vacío")
        elif genero.strip() == "":
            st.error("El género no puede estar vacío")
        elif existe_titulo(titulo):
            st.error("La película ya existe")
        else:
            st.session_state.peliculas.append(
                {
                    "titulo": titulo,
                    "genero": genero,
                    "duracion": duracion,
                    "recaudacion": recaudacion,
                    "puntaje": puntaje,
                }
            )
            st.success(f"'{titulo}' cargada correctamente")

# ----------------------------------------
# Mostrar películas
# ----------------------------------------
elif menu == "Mostrar películas":
    st.subheader("Películas cargadas")

    if not st.session_state.peliculas:
        st.info("No hay películas cargadas")
    else:
        st.dataframe(st.session_state.peliculas, use_container_width=True)

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
        st.dataframe(st.session_state.peliculas, use_container_width=True)

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
            st.write(encontrada)
        else:
            st.warning("La película no existe")

# ----------------------------------------
# Buscar por género
# ----------------------------------------
elif menu == "Buscar por género":
    st.subheader("Buscar películas por género")

    genero = st.text_input("Género a buscar")

    if genero:
        resultado = [p for p in st.session_state.peliculas if p["genero"].lower() == genero.lower()]
        if resultado:
            st.dataframe(resultado, use_container_width=True)
        else:
            st.warning("No hay películas de ese género")

# ----------------------------------------
# Eliminar película
# ----------------------------------------
elif menu == "Eliminar película":
    st.subheader("Eliminar película")

    if not st.session_state.peliculas:
        st.info("No hay películas cargadas")
    else:
        titulos = [p["titulo"] for p in st.session_state.peliculas]
        elegido = st.selectbox("Película a eliminar", titulos)

        if st.button("Eliminar", type="primary"):
            st.session_state.peliculas = [
                p for p in st.session_state.peliculas if p["titulo"] != elegido
            ]
            st.success("Película eliminada correctamente")
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
        col2.metric("Promedio de puntajes", round(sum(puntajes) / len(puntajes), 2))
        col3.metric("Recaudación total", f"${sum(recaudaciones):,.2f}")

        st.write("**Mayor puntaje:**", mayor["titulo"], f"({mayor['puntaje']})")
        st.write("**Menor puntaje:**", menor["titulo"], f"({menor['puntaje']})")
        st.write("**Más taquillera:**", mas_taquillera["titulo"], f"(${mas_taquillera['recaudacion']:,.2f})")
