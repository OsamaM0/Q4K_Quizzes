import speech_recognition as sr
from ..base_interface import IDocumentTextExtractor


class AudioExtractor(IDocumentTextExtractor):
    def extract_text(self, file_path: str) -> str:
        if not file_path.endswith(('.wav', '.flac', '.mp3', '.m4a')):
            raise ValueError("Invalid file type. Expected an audio file (wav, flac, mp3, m4a).")

        recognizer = sr.Recognizer()
        text = ""

        try:
            with sr.AudioFile(file_path) as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data)  # Using Google's speech recognition engine

        except sr.RequestError as e:
            print(f"API request error: {e}")
        except sr.UnknownValueError:
            print("Speech recognition could not understand the audio.")
        except Exception as e:
            print(f"Error in audio extraction: {e}")

        return text
