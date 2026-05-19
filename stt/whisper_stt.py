import whisper
import tempfile

model = whisper.load_model("base")

def transcribe_audio(audio_bytes):

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        f.write(audio_bytes)

        result = model.transcribe(f.name)

    return result["text"]