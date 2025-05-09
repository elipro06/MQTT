import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform

st.markdown("""
    <style>
        .stApp {
            background-color: #121212;
            color: #ffffff;
        }
        h1, h2, h3, h4, h5, h6, p, span, label {
            color: #8e24aa !important;
        }
        .stButton>button {
            font-weight: 600;
            border-radius: 8px;
            padding: 0.7em 1.5em;
            background-color: #6200ea;
            color: #f5f5f5;
            border: none;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #bb86fc;
            color: #000;
        }
        div.stSlider > label {
            color: #ffeb3b !important;
        }
        .stSlider>div>div>div>div>input {
            background-color: #6200ea;
        }
        .stAlert {
            background-color: #3700b3;
            color: #ffffff;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

st.write("🛠️ Plataforma actual:", platform.system(), "| 🐍 Python", platform.python_version())

values = 0.0
act1 = "INACTIVO"

def on_publish(client, userdata, result):
    print("Mensaje enviado exitosamente.")
    pass

def on_message(client, userdata, message):
    global message_received
    time.sleep(1)
    message_received = str(message.payload.decode("utf-8"))
    st.success(f"📩 Mensaje recibido: {message_received}")

broker = "157.230.214.127"
port = 1883
client1 = paho.Client("NEON-CLIENT")
client1.on_message = on_message

st.title("💡 Panel de Control IoT")

col1, col2 = st.columns(2)
with col1:
    if st.button('🔌 Activar dispositivo'):
        act1 = "ACTIVO"
        client1 = paho.Client("NEON-CLIENT")
        client1.on_publish = on_publish
        client1.connect(broker, port)
        message = json.dumps({"Estado": act1})
        ret = client1.publish("cmqtt_s", message)
with col2:
    if st.button('🛑 Desactivar dispositivo'):
        act1 = "INACTIVO"
        client1 = paho.Client("NEON-CLIENT")
        client1.on_publish = on_publish
        client1.connect(broker, port)
        message = json.dumps({"Estado": act1})
        ret = client1.publish("cmqtt_s", message)

st.subheader("🎚️ Control de Intensidad")
values = st.slider('Define el nivel de salida (0 a 100)', 0.0, 100.0, 50.0)
st.write(f"Nivel seleccionado: {values:.1f}")

if st.button('📤 Transmitir valor analógico'):
    client1 = paho.Client("NEON-CLIENT")
    client1.on_publish = on_publish
    client1.connect(broker, port)
    message = json.dumps({"Analogico": float(values)})
    ret = client1.publish("cmqtt_a", message)
