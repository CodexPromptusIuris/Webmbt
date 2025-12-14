import streamlit as st
import pandas as pd

# --- CONFIGURACIÓN GENERAL ---
st.set_page_config(
    page_title="Manualidades Botonería Temuco",
    page_icon="🧶",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILOS VISUALES (MARCA) ---
st.markdown("""
    <style>
    /* Color principal fucsia */
    .stApp a { color: #D63384; }
    .main-title { 
        color: #D63384; 
        font-family: 'Helvetica', sans-serif;
        font-size: 3em; 
        font-weight: 800; 
        text-align: center; 
        text-transform: uppercase;
        margin-bottom: 10px;
    }
    .sub-title {
        text-align: center;
        color: #666;
        font-size: 1.2em;
        margin-bottom: 30px;
    }
    .product-card { 
        background-color: white;
        border: 1px solid #eee; 
        padding: 20px; 
        border-radius: 15px; 
        text-align: center; 
        margin-bottom: 20px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    .product-card:hover {
        transform: scale(1.02);
        border-color: #D63384;
    }
    .price-tag { 
        color: #28a745; 
        font-size: 1.4em; 
        font-weight: bold; 
        margin: 10px 0;
    }
    .stButton>button {
        background-color: #D63384;
        color: white;
        border-radius: 20px;
        border: none;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #b02a6b;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# --- GESTIÓN DEL ESTADO (CARRITO) ---
if 'carro' not in st.session_state:
    st.session_state.carro = []

def agregar_al_carro(item, precio):
    st.session_state.carro.append({"Producto": item, "Precio": precio})
    st.toast(f"✅ {item} agregado al carro", icon="🛒")

def calcular_total():
    return sum(item['Precio'] for item in st.session_state.carro)

# --- BASE DE DATOS DE PRODUCTOS ---
# Basado en tus imágenes subidas
CATALOGO = {
    "🧶 Lanas y Costura": [
        {"nombre": "Lana Reginella (Ovillo)", "precio": 2800, "desc": "Variedad de colores. Calidad clásica.", "img": "🧶"},
        {"nombre": "Cisne TodoDía Colors", "precio": 3500, "desc": "Antipilling, matizado multicolor.", "img": "🌈"},
        {"nombre": "Pack Botones Coloridos", "precio": 1500, "desc": "Botones surtidos para manualidades.", "img": "🔘"},
        {"nombre": "Kit de Agujas/Palillos", "precio": 4000, "desc": "Set básico para tejido.", "img": "🥢"},
    ],
    "🎓 Graduaciones": [
        {"nombre": "Banda 'Príncipe/Princesa'", "precio": 5000, "desc": "Satín brillante. Letras doradas/glitter.", "img": "🤴"},
        {"nombre": "Banda Personalizada 2025", "precio": 6500, "desc": "Con nombre y año. Colores a elección.", "img": "🎖️"},
        {"nombre": "Banda 'Miss' (Certamen)", "precio": 5000, "desc": "Para reinas y eventos escolares.", "img": "👑"},
    ],
    "👼 Bautizo y Recuerdos": [
        {"nombre": "Frasquito Recuerdo (x12)", "precio": 12000, "desc": "Vidrio con mostacillas azules/rosas.", "img": "🍼"},
        {"nombre": "Librito 'Mi Primera Comunión'", "precio": 1500, "desc": "Oraciones básicas. Portada dorada.", "img": "📖"},
        {"nombre": "Angelitos de Porcelana", "precio": 2000, "desc": "Figuritas para decorar tortas o recuerdos.", "img": "👼"},
        {"nombre": "Ramo Flores Rococó", "precio": 2500, "desc": "Flores artificiales pequeñas.", "img": "💐"},
    ],
    "👰 Novias y Fiesta": [
        {"nombre": "Tocado Cristales (Peineta)", "precio": 15000, "desc": "Diseño floral con pedrería fina.", "img": "💎"},
        {"nombre": "Tiara/Corona Strass", "precio": 18000, "desc": "Brillo elegante para novias/quinceañeras.", "img": "🏰"},
        {"nombre": "Guantes Blancos", "precio": 4500, "desc": "Tela suave, tallas estándar.", "img": "🧤"},
        {"nombre": "Liga de Novia", "precio": 3500, "desc": "Encaje blanco tradicional.", "img": "💃"},
    ]
}

# --- BARRA LATERAL ---
with st.sidebar:
    st.title("📌 Menú")
    menu = st.radio("Navegación", ["Inicio", "Catálogo", "Mi Carrito"], label_visibility="collapsed")
    
    st.divider()
    st.subheader("🛍️ Tu Pedido")
    cantidad = len(st.session_state.carro)
    st.metric("Artículos", cantidad)
    st.metric("Total a Pagar", f"${calcular_total():,}")
    
    if cantidad > 0:
        if st.button("Ir a Pagar ➡️"):
            menu = "Mi Carrito" # Redirección forzada
            st.rerun()

    st.divider()
    st.info("📍 Temuco, Chile\n📦 Envíos a todo el país")

# --- PÁGINA: INICIO ---
if menu == "Inicio":
    st.markdown('<div class="main-title">MANUALIDADES BOTONERÍA TEMUCO</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Todo en lanas, accesorios, recuerdos y confección personalizada.</div>', unsafe_allow_html=True)
    
    # Banner de bienvenida
    st.image("https://images.unsplash.com/photo-1606041008023-472dfb5e530f?q=80&w=1000&auto=format&fit=crop", 
             use_container_width=True, caption="Inspiración y Creatividad")

    col1, col2, col3 = st.columns(3)
    col1.warning("🧶 **Lanas Premium**\nReginella, Cisne y más.")
    col2.success("🎓 **Graduaciones**\nBandas personalizadas.")
    col3.info("👼 **Recuerdos**\nBautizos y Comuniones.")

# --- PÁGINA: CATÁLOGO ---
elif menu == "Catálogo":
    st.title("🛒 Catálogo de Productos")
    st.write("Selecciona una categoría para ver nuestros productos disponibles.")
    
    tabs = st.tabs(CATALOGO.keys())
    
    for i, (categoria, productos) in enumerate(CATALOGO.items()):
        with tabs[i]:
            # Grid de 3 columnas
            cols = st.columns(3)
            for index, prod in enumerate(productos):
                with cols[index % 3]:
                    st.markdown(f"""
                    <div class="product-card">
                        <div style="font-size: 60px;">{prod['img']}</div>
                        <h3>{prod['nombre']}</h3>
                        <p style="color: #666; font-size: 0.9em;">{prod['desc']}</p>
                        <div class="price-tag">${prod['precio']:,}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"Agregar al Carro", key=f"btn_{categoria}_{index}"):
                        agregar_al_carro(prod['nombre'], prod['precio'])

# --- PÁGINA: CARRITO ---
elif menu == "Mi Carrito":
    st.title("🛍️ Finalizar Compra")
    
    if len(st.session_state.carro) == 0:
        st.info("Tu carro está vacío. ¡Vuelve al catálogo para vitrinear!")
        if st.button("⬅️ Volver al Catálogo"):
            st.rerun()
    else:
        # Tabla de resumen
        df = pd.DataFrame(st.session_state.carro)
        st.dataframe(df, use_container_width=True)
        
        total = calcular_total()
        st.markdown(f"### Total Final: **${total:,}**")
        
        st.divider()
        st.subheader("Envía tu pedido por WhatsApp")
        st.write("Al hacer clic, se abrirá WhatsApp con el detalle listo para enviar.")
        
        # Formulario de datos básicos
        col_datos1, col_datos2 = st.columns(2)
        cliente = col_datos1.text_input("Tu Nombre", placeholder="Ej: María Pérez")
        telefono_cliente = col_datos2.text_input("Tu Teléfono", placeholder="+569...")
        
        # Generador de Link de WhatsApp
        NUMERO_TIENDA = "56912345678" # <--- ¡CAMBIA ESTO POR TU NÚMERO REAL!
        
        mensaje = f"Hola Botonería Temuco! Soy {cliente}. Me gustaría confirmar este pedido:%0A"
        for item in st.session_state.carro:
            mensaje += f"• {item['Producto']} (${item['Precio']})%0A"
        mensaje += f"%0A*TOTAL: ${total:,}*"
        
        link_wa = f"https://wa.me/{NUMERO_TIENDA}?text={mensaje}"
        
        c1, c2 = st.columns([1, 2])
        with c1:
            if st.button("🗑️ Vaciar Carro"):
                st.session_state.carro = []
                st.rerun()
        with c2:
            if cliente:
                st.link_button("📲 Enviar Pedido por WhatsApp", link_wa, type="primary", use_container_width=True)
            else:
                st.warning("Por favor escribe tu nombre para generar el pedido.")
