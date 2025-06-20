import streamlit as st
from moviepy.editor import VideoFileClip
import tempfile
import os

# Configuração da página
st.set_page_config(page_title="Ajustador de Vídeos OOH", layout="centered")
st.title("🛠️ Ajustador de Vídeos para Painéis OOH")

# Formatos disponíveis
formatos = {
    "768x1152 (Painéis e Empenas Digitais)": (768, 1152),
    "480x1080 (Empena Nossa Sra. do Carmo)": (480, 1080),
    "720x480 (Banca 3x2)": (720, 480),
    "960x480 (Banca 4x2)": (960, 480),
    "1200x480 (Banca 5x2)": (1200, 480),
    "896x288 (Painéis Horizontais)": (896, 288),
    "600x2400 (Empena Praça Portugal)": (600, 2400),
}

formato_escolhido = st.selectbox("📐 Escolha o formato final do vídeo:", list(formatos.keys()))
resolucao = formatos[formato_escolhido]

uploaded_file = st.file_uploader("📁 Envie o vídeo do cliente (MP4)", type=["mp4"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_file_path = temp_file.name

    try:
        st.info("🎬 Processando vídeo...")
        clip = VideoFileClip(temp_file_path)
        target_duration = 10.0

        # Ajustar tempo (loop ou cortar)
        if clip.duration > target_duration:
            clip = clip.subclip(0, target_duration)
        elif clip.duration < target_duration:
            clip = clip.loop(duration=target_duration)

        # Redimensionar (esticando sem preservar aspecto)
        largura, altura = resolucao
        clip = clip.resize(newsize=(largura, altura))

        output_path = temp_file_path.replace(".mp4", "_ajustado.mp4")
        clip.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")

        with open(output_path, "rb") as f:
            st.success("✅ Vídeo ajustado com sucesso!")
            st.download_button("⬇️ Baixar vídeo ajustado", f, file_name="video_ajustado.mp4")

    except Exception as e:
        st.error(f"❌ Erro ao processar o vídeo: {str(e)}")
