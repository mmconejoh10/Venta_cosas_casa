import streamlit as st
import pandas as pd
import os

# ---------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------
st.set_page_config(page_title="Venta nuestras cosas", page_icon="🏠", layout="wide")

# ---------------------------------------------------------------
# GLOBAL CSS – ESTILO PINTEREST MINIMALISTA (OPCIÓN 3)
# ---------------------------------------------------------------
st.markdown(
    """
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;700&family=Nunito:wght@300;400;600;700&display=swap');

    html, body, [data-testid="stApp"] {
        background-color: #f4eee9 !important;
        font-family: 'Nunito', sans-serif;
        color: #4b2e2b !important;
    }

    .block-container {
        max-width: 1120px !important;
        padding-top: 1rem !important;
        padding-bottom: 1.5rem !important;
    }

    /* -------- SIDEBAR: MISMO FONDO Y COLORES QUE EL MAIN -------- */

    [data-testid="stSidebar"] {
        background-color: #f4eee9 !important;
    }

    [data-testid="stSidebar"] > div:first-child {
        background-color: #f4eee9 !important;
    }

    [data-testid="stSidebar"] * {
        color: #4b2e2b !important;
    }

    [data-testid="stSidebar"] input,
    [data-testid="stSidebar"] select {
        background-color: #fffaf5 !important;
        color: #4b2e2b !important;
        border-radius: 8px !important;
        border: 1px solid #e6d6ce !important;
    }

        /* --------- FIX SELECTBOX APPEARANCE --------- */
    [data-testid="stSelectbox"] > div > div {
        background-color: #ffffff !important;     /* Fondo blanco */
        color: #4b2e2b !important;                /* Texto café oscuro */
        border: 1px solid #d8c8bd !important;     /* Borde suave */
        border-radius: 8px !important;
    }

    /* Texto dentro de la lista desplegable */
    [data-testid="stSelectbox"] ul li {
        background-color: #ffffff !important;
        color: #4b2e2b !important;
    }

    /* Hover en la lista */
    [data-testid="stSelectbox"] ul li:hover {
        background-color: #f6eee7 !important;
    }

    /* Header */
    .page-header h1 {
        font-family: 'Playfair Display', serif;
        font-size: 2.4rem;
        color: #4b2e2b;
    }

    .page-header p {
        font-size: 1rem;
        color: #6b4a45;
    }

    /* ---------- PINTEREST MINIMAL STYLE FOR ITEMS ---------- */

    .item-card {
        background: transparent !important;
        border: none !important;
        padding: 2px 2px !important;
        margin-bottom: 18px !important;
        border-radius: 18px !important;
        box-shadow: 0 6px 18px rgba(0,0,0,0.04) !important;
    }

    .item-divider {
        height: 2px;
        background-color: rgba(100, 70, 60, 0.15);
        margin: 8px 0 16px 0;
    }

    /* Título */
    .item-title {
        font-family: 'Playfair Display', serif !important;
        font-size: 1.8rem !important;
        font-weight: 600 !important;
        color: #4b2e2b !important;
        margin-bottom: 0.4rem !important;
        text-align: center !important;
        text-decoration: underline !important;
        text-underline-offset: 6px !important;
    }

    /* Imágenes uniformes */
    .stImage img {
        height: 420px !important;
        width: 100% !important;
        object-fit: contain !important;
        background-color: #f8f3ee !important;
        padding: 6px !important;
        border-radius: 16px !important;
        border: 1px solid #eadfd5 !important;
    }

    /* Precio */
    .price-tag {
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        color: #7a4f45 !important;
        margin-top: 6px !important;
    }

    /* Descripción */
    .item-description {
        font-size: 0.95rem !important;
        color: #533c38 !important;
        line-height: 1.45 !important;
    }

    /* Categoría estilo chip */
    .category-chip {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 999px;
        background-color: #f3dcd3;
        color: #7a4f4a;
        font-size: 12px;
        font-weight: 600;
    }

    /* Enlace referencia */
    .ref-link a {
        color: #b76f5a;
        text-decoration: none !important;
    }

    .ref-link a:hover {
        text-decoration: underline !important;
    }

    /* WhatsApp buttons */
    .wa-btn {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 9px 16px;
        border-radius: 999px;
        text-decoration: none;
        font-size: 13px;
        font-weight: 600;
        margin-right: 8px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.08);
    }

    .wa-btn.primary {
        background-color: #25d366;
        color: white !important;
    }

    .wa-btn.secondary {
        background-color: #eedcd5;
        color: #7b4f4b !important;
    }

    /* Botones (flechas, ver grande, etc.) */
    .stButton > button {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        color: #6b4a45 !important;
        font-size: 18px !important;
    }

    .stButton > button:hover {
        background-color: #f1e6dd !important;
        color: #4b2e2b !important;
        border-radius: 10px !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------
# WHATSAPP NUMBERS
# ---------------------------------------------------------------
MI_WHATSAPP = "50686014903"
ESPOSO_WHATSAPP = "50686434246"


# ---------------------------------------------------------------
# CLEAN ID
# ---------------------------------------------------------------
def clean_id(name, idx):
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

    # Normalizar nombres de columnas (quitar espacios, etc.)
    df.rename(columns={c: c.strip() for c in df.columns}, inplace=True)

    # Unificar "Categoría" -> "Categoria"
    if "Categoría" in df.columns and "Categoria" not in df.columns:
        df["Categoria"] = df["Categoría"]

    # Asegurar columna Categoria exista
    if "Categoria" not in df.columns:
        df["Categoria"] = ""

    # Limpiar valores de Categoria
    df["Categoria"] = df["Categoria"].astype(str).str.strip()
    df.loc[df["Categoria"].isin(["", "nan", "None"]), "Categoria"] = pd.NA

    # Asegurar columna Referencia
    if "Referencia" not in df.columns:
        if "Referencias" in df.columns:
            df["Referencia"] = df["Referencias"]
        else:
            df["Referencia"] = ""

    # Asegurar columna Estado
    if "Estado" not in df.columns:
        df["Estado"] = "Disponible"

    return df


data = load_data()

# ---------------------------------------------------------------
# HEADER
# ---------------------------------------------------------------
st.markdown(
    """
    <div class="page-header">
        <h1>Venta de nuestras cosas</h1>
        <p>Debemos vender todas nuestras pertenencias pues nos mudamos de país.  
        Gracias por verlas, compartirlas y apoyarnos para encontrarle nueva casa a todo 💛</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Línea minimalista debajo del header
st.markdown("<div class='item-divider'></div>", unsafe_allow_html=True)

# ---------------------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------------------
st.sidebar.header("Filtros")

# Filtro de búsqueda libre
search_text = st.sidebar.text_input("Buscar:")

# Filtro de categoría (ya con datos reales)
categorias_unicas = sorted([c for c in data["Categoria"].dropna().unique()])
categorias = ["Todas"] + categorias_unicas
categoria_filtro = st.sidebar.selectbox("Categoría:", categorias)

# Filtro de disponibilidad
estados = ["Todos", "Disponible", "Vendido"]
estado_filtro = st.sidebar.radio("Estado:", estados)

# ---------------------------------------------------------------
# APLICAR FILTROS
# ---------------------------------------------------------------
filtered = data.copy()

# Filtro por texto
if search_text.strip():
    mask = filtered["Nombre"].astype(str).str.contains(
        search_text, case=False, na=False
    ) | filtered["Descripcion"].astype(str).str.contains(
        search_text, case=False, na=False
    )
    filtered = filtered[mask]

# Filtro por categoría
if categoria_filtro != "Todas":
    filtered = filtered[filtered["Categoria"] == categoria_filtro]

# Filtro por estado (disponible / vendido)
if estado_filtro != "Todos":
    filtered = filtered[filtered["Estado"] == estado_filtro]


# ---------------------------------------------------------------
# MODAL
# ---------------------------------------------------------------
def show_modal(images, modal_key):
    idx = st.session_state[modal_key]

    st.image(images[idx], width="stretch")

    left, center, right = st.columns([1, 4, 1])

    with left:
        if st.button("⬅️", key=f"modal_prev_{modal_key}", use_container_width=True):
            st.session_state[modal_key] = (idx - 1) % len(images)

    with center:
        st.markdown(
            f"<div style='text-align:center;color:#6b4a45;'>Foto {idx + 1} de {len(images)}</div>",
            unsafe_allow_html=True,
        )

    with right:
        if st.button("➡️", key=f"modal_next_{modal_key}", use_container_width=True):
            st.session_state[modal_key] = (idx + 1) % len(images)

    if st.button("❌ Cerrar vista grande", key=f"close_{modal_key}"):
        st.session_state.pop(modal_key)


# ---------------------------------------------------------------
# DISPLAY ITEM
# ---------------------------------------------------------------
def show_item(row, idx):
    st.markdown("<div class='item-card'>", unsafe_allow_html=True)

    item_id = clean_id(row["Nombre"], idx)
    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown(
            f"<div class='item-title'>{row['Nombre']}</div>", unsafe_allow_html=True
        )

        imgs = [i.strip() for i in str(row["Imagenes"] or "").split(",") if i.strip()]
        paths = [
            os.path.join("images", img)
            for img in imgs
            if os.path.exists(os.path.join("images", img))
        ]

        if paths:
            key = f"main_{item_id}"
            if key not in st.session_state:
                st.session_state[key] = 0

            current = st.session_state[key]

            left, center, right = st.columns([1, 4, 1])

            with left:
                if st.button("⬅️", key=f"prev_{item_id}", use_container_width=True):
                    st.session_state[key] = (current - 1) % len(paths)

            with center:
                st.markdown(
                    f"<div style='text-align:center;color:#6b4a45;'>Foto {st.session_state[key] + 1} de {len(paths)}</div>",
                    unsafe_allow_html=True,
                )

            with right:
                if st.button("➡️", key=f"next_{item_id}", use_container_width=True):
                    st.session_state[key] = (current + 1) % len(paths)

            st.image(paths[st.session_state[key]], width="stretch")

            if st.button("🔍 Ver grande", key=f"zoom_{item_id}"):
                st.session_state[f"modal_{item_id}"] = st.session_state[key]

            modal_key = f"modal_{item_id}"
            if modal_key in st.session_state:
                st.markdown("---")
                st.subheader("Vista ampliada")
                show_modal(paths, modal_key)

        else:
            st.info("No hay imágenes disponibles")

        video = row.get("Video", "")
        if isinstance(video, str) and video.strip():
            vp = os.path.join("videos", video.strip())
            if os.path.exists(vp):
                st.video(vp)

    with col2:
        if str(row["Categoria"]).strip():
            st.markdown(
                f"<div class='category-chip'>{row['Categoria']}</div>",
                unsafe_allow_html=True,
            )

        # Estado (Disponible / Vendido)
        estado = str(row.get("Estado", "")).strip()
        if estado:
            color = "#4CAF50" if estado == "Disponible" else "#B84C4C"
            st.markdown(
                f"<div style='padding:4px 12px;display:inline-block;border-radius:999px;"
                f"background-color:{color}20;color:{color};font-size:12px;font-weight:700;margin-left:8px;'>"
                f"{estado}"
                f"</div>",
                unsafe_allow_html=True,
            )

        precio_str = f"₡{int(row['Precio']):,}".replace(",", ".")
        st.markdown(
            f"<div class='price-tag'>{precio_str}</div>", unsafe_allow_html=True
        )

        st.write(f"**Modelo:** {row['Modelo']}")

        st.markdown(
            f"<div class='item-description'>{row['Descripcion']}</div>",
            unsafe_allow_html=True,
        )

        ref = str(row.get("Referencia", "")).strip()
        if ref not in ["", "nan", "None"]:
            st.markdown(
                f"<div class='ref-link'><a href='{ref}' target='_blank'>🌐 Ver más detalles</a></div>",
                unsafe_allow_html=True,
            )

        st.markdown("#### Contacto por WhatsApp")

        encoded = row["Nombre"].replace(" ", "%20")
        msg = f"Hola,%20estoy%20interesad@%20en%20este%20artículo:%20{encoded}"

        st.markdown(
            f"<a class='wa-btn primary' href='https://wa.me/{MI_WHATSAPP}?text={msg}' target='_blank'>📲 Contactar a Moni</a>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<a class='wa-btn secondary' href='https://wa.me/{ESPOSO_WHATSAPP}?text={msg}' target='_blank'>📲 Contactar a Fabi</a>",
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------------------------------
# RENDER ALL
# ---------------------------------------------------------------
if filtered.empty:
    st.warning("No se encontraron resultados.")
else:
    for idx, row in filtered.reset_index(drop=True).iterrows():
        show_item(row, idx)
        st.markdown("<div class='item-divider'></div>", unsafe_allow_html=True)

st.caption("Aplicación creada por Mónica 💕")
