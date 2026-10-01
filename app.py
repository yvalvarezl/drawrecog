import base64
import io
from PIL import Image
import streamlit as st
from streamlit_drawable_canvas import st_canvas
from openai import OpenAI

# ---------------------------------------------------------
# Configuración de la página
# ---------------------------------------------------------
st.set_page_config(
    page_title="Lienzo Estelar 🌌",
    page_icon="✨",
    layout="wide"
)

# ---------------------------------------------------------
# Barra Lateral: Configuración del Observatorio
# ---------------------------------------------------------
st.sidebar.title("🌌 Observatorio Estelar")
st.sidebar.caption("Configura tus herramientas astronómicas")

st.sidebar.markdown("---")

# Campo de entrada para la API Key
api_key_input = st.sidebar.text_input(
    "🔑 OpenAI API Key",
    type="password",
    placeholder="Pega tu clave (sk-...) aquí",
    help="Ingresa tu API Key para activar la interpretación con IA."
)

st.sidebar.markdown("---")
st.sidebar.subheader("🎨 Herramientas Astronómicas")

stroke_width = st.sidebar.slider("Grosor del rayo estelar", 1, 30, 8)
stroke_color = st.sidebar.color_picker("Color de estrella", "#000000")
bg_color = st.sidebar.color_picker("Color del cosmos", "#FFFFFF")

drawing_mode = st.sidebar.selectbox(
    "Herramienta Estelar:",
    ("freedraw", "line", "circle", "rect")
)

# ---------------------------------------------------------
# Encabezado Principal
# ---------------------------------------------------------
st.title("✨ Lienzo Estelar: Interpretación de Constelaciones 🌌")
st.write("Dibuja tu constelación o figura en el lienzo y deja que el observatorio espacial analice su significado con IA.")

col_canvas, col_analysis = st.columns([1, 1], gap="large")

with col_canvas:
    st.subheader("🖼️ El Lienzo Cósmico")
    
    canvas_result = st_canvas(
        fill_color="rgba(255, 255, 255, 0)",
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=bg_color,
        height=380,
        width=380,
        drawing_mode=drawing_mode,
        key="canvas_estelar",
    )

with col_analysis:
    st.subheader("🤖 Revelación Astronómica")
    
    analyze_btn = st.button("✨ Analizar Constelación", type="primary", use_container_width=True)
    
    if analyze_btn:
        if not api_key_input:
            st.warning("⚠️ Ingresa tu OpenAI API Key en la barra lateral para realizar el análisis.")
        elif canvas_result.image_data is not None:
            # Procesar imagen del lienzo
            img_data = canvas_result.image_data
            img = Image.fromarray(img_data.astype("uint8")).convert("RGB")
            
            # Convertir a Base64
            buffered = io.BytesIO()
            img.save(buffered, format="JPEG")
            base64_image = base64.b64encode(buffered.getvalue()).decode("utf-8")
            
            # Consulta a OpenAI Vision
            client = OpenAI(api_key=api_key_input)
            
            # Prompt estructurado en tres partes
            prompt_estelar = (
                "Actúa como un astrónomo poético, narrador místico y sabio del cosmos. "
                "Analiza el dibujo adjunto y genera una respuesta estructurada en exactamente 3 secciones usando Markdown:\n\n"
                "1. **👀 ¿Qué revelan las estrellas?:** Describe muy brevemente (en 1 o 2 frases) qué forma o trazo ves en el dibujo.\n"
                "2. **🌌 La Leyenda de la Constelación:** Inventa una historia o mito fantástico sobre el origen de esta constelación. Incluye detalles mágicos, qué simboliza en el universo o qué leyenda cuentan los antiguos astrónomos sobre ella.\n"
                "3. **✨ Un mensaje del Firmamento:** Termina con un mensaje caluroso de felicitación para el autor del dibujo, elogiando su belleza y creatividad con palabras bonitas y emojis alegres."
            )
            
            try:
                with st.spinner("Leyendo las estrellas y descifrando la leyenda... 🔭"):
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": prompt_estelar},
                                    {
                                        "type": "image_url",
                                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                                    }
                                ]
                            }
                        ],
                        max_tokens=600
                    )
                    
                    resultado = response.choices[0].message.content
                    st.success("¡Constelación descifrada!")
                    st.markdown(resultado)
                    st.balloons()  # ¡Efecto de globos para celebrar!
                    
            except Exception as e:
                st.error(f"Error al conectar con el observatorio: {e}")
        else:
            st.info("👆 Dibuja una figura sobre el lienzo antes de analizar.")
