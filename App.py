import streamlit as st
import pandas as pd
from PIL import Image
import os

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Manualidades Botonería Temuco",
    page_icon="🧶",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILOS CSS (PERSONALIZADO ROSADO/FUCSIA) ---
st.markdown("""
    <style>
    /* Color principal basado en tu logo (#D63384 aprox) */
    .stApp a { color: #E91E63; }
    
    .main-header { 
        text-align: center; 
        padding: 20px;
    }
    
    .product-card { 
        background-color: white;
        border: 1px solid #f0f0f0; 
        padding: 15px; 
        border-radius: 10px; 
        text-align: center; 
        margin-bottom: 20px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transition: transform 0.2s;
    }
    .product-card:hover {
        transform: scale(1.03);
        border: 1px solid #E91E63;
        box-shadow: 0 8px 15px rgba(233, 30, 99, 0.2);
    }
    
    .price-tag { 
        color: #2E7D32; 
        font-size: 1.3em; 
        font-weight: bold; 
        margin-top: 10px;
    }
    
    .category-header {
        color: #E91E63;
        border-bottom: 2px solid #E91E63;
        padding-bottom: 10px;
        margin-top: 20px;
    }
    
    /* Botones personalizados */
    .stButton>button {
        background-color: #E91E63;
        color: white;
        border-radius: 20px;
        border: none;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #C2185B;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# --- GESTIÓN DEL CARRITO (SESSION STATE) ---
if 'carro' not in st.session_state:
    st.session_state.carro = []

def agregar_al_carro(item, precio):
    st.session_state.carro.append({"Producto": item, "Precio": precio})
    st.toast(f"✅ {item} agregado!", icon="🛍️")

def calcular_total():
    return sum(item['Precio'] for item in st.session_state.carro)

# --- DATOS DE PRODUCTOS (EXTRAÍDOS DE TUS FOTOS) ---
CATALOGO = {
    "🧶 Tejido y Lanas": [
        {"nombre": "Lana Reginella (Ovillo)", "precio": 2800, "desc": "Carta de colores completa: Beige, Rojo, Fucsia, Gris...", "img": "🧶"},
        {"nombre": "Cisne TodoDía Colors", "precio": 3500, "desc": "Hilado matizado multicolor, antipilling.", "img": "🌈"},
        {"nombre": "Palillos / Crochet", "precio": 2500, "desc": "Diferentes medidas para tus proyectos.", "img": "🥢"},
    ],
    "🎓 Graduaciones y Bandas": [
        {"nombre": "Banda 'Príncipe' Azul", "precio": 5000, "desc": "Satín azul rey con letras glitter/doradas.", "img": "🤴"},
        {"nombre": "Banda 'Princesa' Rosa/Blanca", "precio": 5000, "desc": "Satín suave, letras elegantes.", "img": "👸"},
        {"nombre": "Banda Personalizada + Año", "precio": 6500, "desc": "Ej: 'Miss Arlette 2025'. Nombre y año a elección.", "img": "🎓"},
        {"nombre": "Banda 'Miss' Certamen", "precio": 5000, "desc": "Para concursos y reinas de alianzas.", "img": "👑"},
    ],
    "👼 Recuerdos y Ceremonias": [
        {"nombre": "Frasquito Bautizo (x12)", "precio": 12000, "desc": "Recuerdo vidrio con mostacillas azules/rosas y tarjeta.", "img": "🍼"},
        {"nombre": "Librito 'Mi Primera Comunión'", "precio": 1500, "desc": "Oraciones y sacramentos. Portada dorada.", "img": "📖"},
        {"nombre": "Angelito Porcelana", "precio": 2200, "desc": "Figura delicada para recuerdos o tortas.", "img": "👼"},
        {"nombre": "Ramo Flores Rococó", "precio": 2500, "desc": "Ramo pequeño de flores artificiales (varios colores).", "img": "💐"},
    ],
    "👰 Novias y Fiesta": [
        {"nombre": "Tocado Cristal Plata", "precio": 15900, "desc": "Peineta con pedrería y diseño floral.", "img": "💎"},
        {"nombre": "Tiara / Corona Strass", "precio": 18900, "desc": "Estilo princesa, brillo intenso.", "img": "🏰"},
        {"nombre": "Guantes Blancos", "precio": 4500, "desc": "Talla estándar, tela lycra/satín.", "img": "🧤"},
        {"nombre": "Liga de Novia", "precio": 3900, "desc": "Encaje blanco con detalle floral.", "img": "💃"},
    ],
    "🪡 Costura y Bordado": [
        {"nombre": "Set de Hilos", "precio": 3000, "desc": "Colores básicos para costura.", "img": "🧵"},
        {"nombre": "Botones Surtidos", "precio": 1500, "desc": "Pack de botones coloridos y creativos.", "img": "🔘"},
        {"nombre": "Cintas de Satín (Rollo)", "precio": 2000, "desc": "Diferentes anchos y colores.", "img": "🎀"},
    ]
}

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("📌 Navegación")
    opcion = st.radio("Ir a:", ["Inicio", "Catálogo Completo", "Ver Carrito"], label_visibility="collapsed")
    
    st.divider()
    
    # Resumen del carrito
    st.subheader("🛍️ Tu Carrito")
    num_items = len(st.session_state.carro)
    if num_items > 0:
        st.write(f"Tienes **{num_items}** productos.")
        st.write(f"Total: **${calcular_total():,}**")
        if st.button("Pagar Ahora ➡️"):
            opcion = "Ver Carrito"
            st.rerun()
    else:
        st.caption("El carrito está vacío.")

    st.divider()
    st.write("📍 **Ubicación:** Temuco, Chile")
    st.write("📸 **Instagram:** [@botoneriatemuco](https://www.instagram.com/botoneriatemuco)")

# --- PÁGINA: INICIO ---
if opcion == "Inicio":
    # LOGO CENTRAL - Aquí buscamos el archivo logo.png
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Intentamos cargar el logo, si no existe mostramos texto
        if os.path.exists("logo.png"):
            st.image("logo.png", use_container_width=True)
        else:
            st.markdown("<h1 style='text-align: center; color: #E91E63;'>MANUALIDADES BOTONERÍA TEMUCO</h1>", unsafe_allow_html=True)
            st.warning("⚠️ Nota: Guarda tu imagen como 'logo.png' en la carpeta para verla aquí.")

    st.markdown("<h3 style='text-align: center; color: #666;'>Tu espacio de creación, lanas, hilos y detalles inolvidables.</h3>", unsafe_allow_html=True)
    
    st.divider()
    
    # Banner de categorías (Iconos grandes)
    c1, c2, c3, c4 = st.columns(4)
    c1.info("🧶 **Tejido**\nReginella y Cisne")
    c2.error("🎓 **Graduación**\nBandas Personalizadas")
    c3.success("👼 **Recuerdos**\nBautizo y Comunión")
    c4.warning("👰 **Novias**\nTocados y Accesorios")

    st.write("---")
    st.markdown("### 🌟 Lo más buscado")
    st.write("Explora nuestro catálogo para encontrar el detalle perfecto para tu evento o tu próximo proyecto de manualidades.")

# --- PÁGINA: CATÁLOGO ---
elif opcion == "Catálogo Completo":
    st.title("🛒 Catálogo de Productos")
    
    # Pestañas por categoría
    categorias = list(CATALOGO.keys())
    tabs = st.tabs(categorias)
    
    for i, categoria in enumerate(categorias):
        with tabs[i]:
            st.markdown(f"<h3 class='category-header'>{categoria}</h3>", unsafe_allow_html=True)
            
            # Grid de productos (3 columnas)
            cols = st.columns(3)
            productos = CATALOGO[categoria]
            
            for idx, prod in enumerate(productos):
                with cols[idx % 3]:
                    st.markdown(f"""
                    <div class="product-card">
                        <div style="font-size: 50px; margin-bottom: 10px;">{prod['img']}</div>
                        <div style="font-weight: bold; font-size: 1.1em;">{prod['nombre']}</div>
                        <div style="color: #777; font-size: 0.9em; min-height: 40px;">{prod['desc']}</div>
                        <div class="price-tag">${prod['precio']:,}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Clave única para el botón
                    btn_key = f"add_{categoria}_{idx}"
                    if st.button("Añadir al Carrito 🛒", key=btn_key):
                        agregar_al_carro(prod['nombre'], prod['precio'])

# --- PÁGINA: CARRITO ---
elif opcion == "Ver Carrito":
    st.title("🛍️ Finalizar Pedido")
    
    if len(st.session_state.carro) == 0:
        st.info("Tu carrito está vacío. ¡Vuelve al catálogo para agregar productos!")
        if st.button("⬅️ Volver a comprar"):
            st.rerun()
    else:
        # Tabla de resumen
        df_carro = pd.DataFrame(st.session_state.carro)
        st.table(df_carro)
        
        total = calcular_total()
        st.markdown(f"<h2 style='text-align: right; color: #E91E63;'>Total a Pagar: ${total:,}</h2>", unsafe_allow_html=True)
        
        st.divider()
        st.subheader("📩 Enviar pedido por WhatsApp")
        st.write("Completa tus datos para generar el enlace automático:")
        
        c1, c2 = st.columns(2)
        nombre = c1.text_input("Tu Nombre")
        telefono = c2.text_input("Tu Teléfono (Opcional)")
        
        # Lógica de WhatsApp
        NUMERO_TIENDA = "56912345678" # <--- ¡PON AQUÍ TU NÚMERO REAL!
        
        mensaje = f"Hola Botonería Temuco! Soy {nombre}. Quisiera confirmar el siguiente pedido:%0A"
        for item in st.session_state.carro:
            mensaje += f"• {item['Producto']} (${item['Precio']})%0A"
        mensaje += f"%0A*TOTAL FINAL: ${total:,}*"
        
        url_wa = f"https://wa.me/{NUMERO_TIENDA}?text={mensaje}"
        
        col_btn1, col_btn2 = st.columns([1, 2])
        
        with col_btn1:
            if st.button("🗑️ Vaciar Carrito"):
                st.session_state.carro = []
                st.rerun()
        
        with col_btn2:
            if nombre:
                st.link_button("📲 Enviar Pedido por WhatsApp", url_wa, type="primary", use_container_width=True)
            else:
                st.warning("⚠️ Por favor escribe tu nombre para continuar.")

