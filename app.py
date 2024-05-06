import streamlit as st
import requests
from io import BytesIO
from tempfile import NamedTemporaryFile

# Function to make API call to Resemble Enhance service
def enhance_audio(input_audio):
    url = "http://localhost:5000/predictions"
    payload = {
        "input": {
            "solver": "Midpoint",
            "input_audio": input_audio,
            "denoise_flag": False,
            "prior_temperature": 0.5,
            "number_function_evaluations": 64
        }
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to enhance audio. Please try again."}

# Streamlit app
def main():
    st.title("Audio Enhancer")
    st.markdown("Developed by Suraj")

    # File uploader for input audio
    st.markdown("### Upload Audio File")
    uploaded_file = st.file_uploader("Choose an audio file", type=["mp3", "wav"])

    # Button to enhance audio
    if st.button("Enhance Audio") and uploaded_file is not None:
        st.text("Enhancing audio...")
        with NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file.close()
            result = enhance_audio(tmp_file.name)
            if "error" in result:
                st.error(result["error"])
            else:
                enhanced_audio = result["enhanced_audio"]
                st.audio(enhanced_audio, format="audio/mp3")

if __name__ == "__main__":
    main()
