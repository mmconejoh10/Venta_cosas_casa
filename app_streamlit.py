import streamlit as st
import pandas as pd
import os

# ---------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------
st.set_page_config(page_title="Venta de mis cosas", page_icon="🏠", layout="wide")

# CSS para fotos y para layout centrado de navegación
st.markdown(
    """
    <style>

    /* Imágenes uniformes */
    .stImage img {
        height: 420px !important;
        width: 100% !important;
        object-fit: contain !important;
        background-color: #f5f5f5;
        padding: 8px;
        border-radius: 10px;
    }

    /* Contenedor centrado para flechas y texto */
    .photo-nav-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 6px; /* flechas pegadas */
        margin: 6px 0 12px 0;
        font-size: 15px;
        font-weight: 500;
        color: #444;
    }

    /* Quitamos padding interno que Streamlit añade alrededor de columns */
    div[data-testid="column"] {
        padding: 0 !important;
    }

    /* Hacemos los botones minimalistas */
    .nav-btn > button {
        background: none !important;
        border: none !important;
        font-size: 20px !important;
        padding: 0 !important;
        line-height: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

MI_WHATSAPP = "50688888888"
ESPOSO_WHATSAPP = "50677777777"


# ---------------------------------------------------------------
# UNIQUE ID
# ---------------------------------------------------------------
def item_id_from_name_and_index(name: str, idx: int) -> str:
    clean = (
        str(name)
        .lower()
        .replace(" ", "_")
        .replace(".", "")
        .replace(",", "")
        .replace("-", "_")
        .replace("/", "_")
    )
    return f"{idx}_{clean}"


# ---------------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("data.xlsx")
    for col in ["Categoria", "Referencia"]:
        if col not in df.columns:
            df[col] = ""
    return df


data = load_data()


# ---------------------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------------------
st.sidebar.header("Filtros")

search_text = st.sidebar.text_input("Buscar:")
categorias = ["Todas"] + sorted(list(data["Categoria"].dropna().unique()))
categoria_filtro = st.sidebar.selectbox("Categoría:", categorias)

filtered = data.copy()

if search_text.strip():
    mask = filtered["Nombre"].astype(str).str.contains(
        search_text, case=False, na=False
    ) | filtered["Descripcion"].astype(str).str.contains(
        search_text, case=False, na=False
    )
    filtered = filtered[mask]

if categoria_filtro != "Todas":
    filtered = filtered[filtered["Categoria"] == categoria_filtro]


# ---------------------------------------------------------------
# FULLSCREEN MODAL
# ---------------------------------------------------------------
def show_modal(images, modal_key):
    st.markdown("---")
    st.subheader("Vista ampliada")

    current = st.session_state[modal_key]

    # FLECHAS + TEXTO CENTRADOS (sin formularios)
    nav_cols = st.columns([1, 4, 1])

    # izquierda
    with nav_cols[0]:
        if st.button("⬅️", key=f"modal_prev_{modal_key}"):
            st.session_state[modal_key] = (current - 1) % len(images)

    # texto centrado
    with nav_cols[1]:
        st.markdown(
            f"""
            <div class="photo-nav-container">
                Foto {current + 1} de {len(images)}
            </div>
            """,
            unsafe_allow_html=True,
        )

    # derecha
    with nav_cols[2]:
        if st.button("➡️", key=f"modal_next_{modal_key}"):
            st.session_state[modal_key] = (current + 1) % len(images)

    current = st.session_state[modal_key]

    st.image(images[current], use_container_width=True)

    if st.button("❌ Cerrar vista grande", key=f"close_modal_{modal_key}"):
        st.session_state.pop(modal_key)


# ---------------------------------------------------------------
# DISPLAY ITEM
# ---------------------------------------------------------------
def show_item(row: pd.Series, idx: int):
    st.markdown("---")

    item_id = item_id_from_name_and_index(row["Nombre"], idx)

    col1, col2 = st.columns([3, 2])

    # ------------------ LEFT SIDE ------------------
    with col1:
        st.subheader(row["Nombre"])

        imgs = [i.strip() for i in str(row["Imagenes"] or "").split(",") if i.strip()]
        full_paths = [
            os.path.join("images", img)
            for img in imgs
            if os.path.exists(os.path.join("images", img))
        ]

        if not full_paths:
            st.info("No hay imágenes disponibles.")
            return

        main_key = f"main_{item_id}"
        if main_key not in st.session_state:
            st.session_state[main_key] = 0

        current = st.session_state[main_key]

        # FLECHAS PEGADAS AL TEXTO (sin formularios)
        nav_cols = st.columns([1, 4, 1])

        # izquierda
        with nav_cols[0]:
            if st.button("⬅️", key=f"main_prev_{item_id}"):
                st.session_state[main_key] = (current - 1) % len(full_paths)

        # texto centrado
        with nav_cols[1]:
            st.markdown(
                f"""
                <div class="photo-nav-container">
                    Foto {current + 1} de {len(full_paths)}
                </div>
                """,
                unsafe_allow_html=True,
            )

        # derecha
        with nav_cols[2]:
            if st.button("➡️", key=f"main_next_{item_id}"):
                st.session_state[main_key] = (current + 1) % len(full_paths)

        current = st.session_state[main_key]
        st.image(full_paths[current], use_container_width=True)

        if st.button("🔍 Ver grande", key=f"zoom_{item_id}"):
            st.session_state[f"modal_{item_id}"] = current

        modal_key = f"modal_{item_id}"
        if modal_key in st.session_state:
            show_modal(full_paths, modal_key)

        # Video seguro
        video_value = row.get("Video", "")
        if isinstance(video_value, str) and video_value.strip():
            vpath = os.path.join("videos", video_value.strip())
            if os.path.exists(vpath):
                st.video(vpath)

    # ------------------ RIGHT SIDE ------------------
    with col2:
        st.write(f"**Modelo:** {row['Modelo']}")
        st.write(f"**Precio:** ₡{int(row['Precio']):,}".replace(",", "."))
        st.write(f"**Categoría:** {row['Categoria']}")
        st.write(row["Descripcion"])

        if str(row["Referencia"]).strip():
            st.markdown(f"[🌐 Ver detalles del fabricante]({row['Referencia']})")

        st.markdown("### Contacto por WhatsApp")

        articulo_encoded = row["Nombre"].replace(" ", "%20")
        msg_encoded = (
            f"Hola,%20estoy%20interesad@%20en%20este%20artículo:%20{articulo_encoded}"
        )

        st.markdown(
            f"[📲 Contactar a Mónica](https://wa.me/{MI_WHATSAPP}?text={msg_encoded})"
        )
        st.markdown(
            f"[📲 Contactar a mi esposo](https://wa.me/{ESPOSO_WHATSAPP}?text={msg_encoded})"
        )


# ---------------------------------------------------------------
# RENDER ALL
# ---------------------------------------------------------------
if filtered.empty:
    st.warning("No se encontraron resultados.")
else:
    for idx, row in filtered.reset_index(drop=True).iterrows():
        show_item(row, idx)

st.markdown("---")
st.caption("Aplicación creada por Mónica 💕")
