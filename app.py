import streamlit as st
import numpy as np
from scipy.io.wavfile import write
import io

def generate_audio(frequency=440, duration=1, sample_rate=44100, volume=0.5):
    """Generate a simple sine wave audio"""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    audio = volume * np.sin(2 * np.pi * frequency * t)
    return audio, sample_rate

def save_audio_to_bytes(audio, sample_rate):
    """Convert audio to bytes for playback"""
    bytes_wav = bytes()
    byte_io = io.BytesIO(bytes_wav)
    write(byte_io, sample_rate, audio)
    return byte_io

st.title("Audio Generation and Playback in Streamlit")

# Parameters
col1, col2 = st.columns(2)
with col1:
    frequency = st.slider("Frequency (Hz)", 100, 1000, 440)
    duration = st.slider("Duration (seconds)", 0.1, 5.0, 1.0)
with col2:
    sample_rate = st.selectbox("Sample Rate", [44100, 22050, 11025], index=0)
    volume = st.slider("Volume", 0.1, 1.0, 0.5)

# Generate and play audio
if st.button("Generate and Play Audio"):
    audio, sr = generate_audio(frequency, duration, sample_rate, volume)
    
    # Convert to bytes for playback
    audio_bytes = save_audio_to_bytes((audio * 32767).astype(np.int16), sr)
    
    # Display audio player
    st.audio(audio_bytes, format='audio/wav')
    
    # Option to download
    st.download_button(
        label="Download WAV file",
        data=audio_bytes,
        file_name="generated_audio.wav",
        mime="audio/wav"
    )
    
    # Display waveform
    st.line_chart(audio[:1000])  # Show first 1000 samples for visualization
