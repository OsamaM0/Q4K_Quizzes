import os
import logging
import speech_recognition as sr
from pydub import AudioSegment
import asyncio
from concurrent.futures import ProcessPoolExecutor
from langdetect import detect  # Language detection

logger = logging.getLogger()

class AudioExtractor:

    async def extract_text(self, audio_path: str) -> str:
        try:
            if not audio_path.endswith(('.wav', '.flac', '.mp3', '.m4a')):
                return False, "Unsupported audio format for STT"

            # Convert MP3 to WAV format if needed
            wav_path = await self.convert_to_wav(audio_path) if audio_path.endswith('.mp3') else audio_path

            if not wav_path:
                return False, "Failed to convert audio to WAV format"

            # Perform STT using the converted WAV audio
            transcription = await self.transcribe_audio(wav_path)

            os.remove(wav_path)  # Remove the temporary WAV file

            return transcription if transcription else (False, "STT failed or returned no text")

        except Exception as e:
            logger.error(e)
            return False, f"Error during extraction: {e}"

    async def convert_to_wav(self, audio_path):
        """Convert MP3 to WAV using ffmpeg"""
        try:
            wav_path = audio_path.replace('.mp3', '.wav')

            command = [
                "ffmpeg", "-y",  # Overwrite output file
                "-i", audio_path,  # Input file
                "-vn",  # No video
                wav_path  # Output file
            ]

            process = await asyncio.create_subprocess_exec(
                *command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await process.communicate()

            if process.returncode == 0:
                logger.info(f"Successfully converted {audio_path} to {wav_path}")
                return wav_path
            else:
                logger.error(f"ffmpeg conversion failed: {stderr.decode()}")
                return False

        except Exception as e:
            logger.error(f"Error in conversion: {e}")
            return False

    async def transcribe_audio(self, audio_path):
        """Transcribe audio to text in asynchronous chunks"""
        try:
            recognizer = sr.Recognizer()
            audio = AudioSegment.from_wav(audio_path)
            duration_ms = len(audio)  # Duration in milliseconds
            chunk_size_ms = 10000  # 10 seconds per chunk

            transcript = ""
            logger.info(f"Transcribing audio in {chunk_size_ms / 1000} second chunks")

            tasks = [
                self.transcribe_chunk(audio[start:start + chunk_size_ms], audio_path, recognizer, start)
                for start in range(0, duration_ms, chunk_size_ms)
            ]
            chunk_transcripts = await asyncio.gather(*tasks)

            transcript = " ".join(chunk_transcripts)
            logger.info("Completed transcription.")
            return transcript

        except Exception as e:
            logger.error(f"Error during transcription: {e}")
            return False

    async def transcribe_chunk(self, chunk_audio, audio_path, recognizer, start):
        """Transcribe a single chunk asynchronously using SpeechRecognition"""
        chunk_path = f"{audio_path}_{start}.wav"
        chunk_audio.export(chunk_path, format="wav")

        loop = asyncio.get_event_loop()
        try:
            chunk_transcript = await loop.run_in_executor(None, self.process_chunk, chunk_path, recognizer)
            os.remove(chunk_path)  # Clean up temporary files
            return chunk_transcript or ""
        except Exception as e:
            logger.error(f"Error processing chunk: {e}")
            os.remove(chunk_path)
            return ""

    def process_chunk(self, chunk_path, recognizer):
        """Process a chunk of audio using Google Web Speech API in a synchronous context"""
        try:
            with sr.AudioFile(chunk_path) as source:
                audio_data = recognizer.record(source)

            initial_transcript = recognizer.recognize_google(audio_data, language="ar")
            detected_lang = detect(initial_transcript)

            logger.info(f"Detected language: {detected_lang}")

            final_transcript = recognizer.recognize_google(
                audio_data, language="en" if detected_lang == 'en' else "ar"
            )

            return final_transcript

        except sr.UnknownValueError:
            logger.warning("Google STT could not understand the audio")
            return ""
        except sr.RequestError as e:
            logger.error(f"STT request failed: {e}")
            return ""
