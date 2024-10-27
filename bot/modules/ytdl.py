import os
import re
import logging
import time

import speech_recognition as sr
from pytubefix import YouTube, Search
from pytubefix.cli import on_progress
import random
logger = logging.getLogger()


class PYTUBE:

    po = ("CgtuWVZIRlU0bGlPOCiO-_q4BjIKCgJFRxIEGgAgLw%3D%3D",
          "MnRA2vCqsWsbd0Di7PiNUMXueFvEoaOMNAHjUnqA2EqQDx0OaDsLQSIQ3yC32PLjN9lG0kBbBmMGf5diAm0FryTQKYi6XudCYS7E2-nkgLTOp2CA6OZoG3q5FCWo3HJ8c-Rvlnmm_TIVLSqjkXHsNTZE2p9K4Q==")
    async def ytdl(url, extention: str = "mp4"):
        for i in range(5):
            try:
                logger.info("Starting Download...")
                yt = YouTube(url, on_progress_callback=on_progress, po_token_verifier=PYTUBE.po, use_po_token=True )
                title = yt.title

                # Create "download" directory if it doesn't exist
                output_folder = "download"
                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)

                # Sanitize title to remove invalid characters for file names
                safe_title = re.sub(r'[\/:*?"<>|]', '', title)
                output_file_path = f"{output_folder}/{safe_title}"

                if extention == "mp3":
                    output_file_path += ".mp3"
                    progressive = False
                    ys = yt.streams.get_audio_only()
                    if not ys:
                        logger.info(f"No audio stream found for bitrate: {format}")
                        return False, f"No audio stream found for bitrate {format}"
                    ys.download(output_path=output_folder, mp3=True)
                    return title, output_file_path

                elif extention == "mp4":
                    output_file_path += ".mp4"
                    progressive = True
                    ys = yt.streams.get_highest_resolution(progressive=progressive)
                    if not ys:
                        logger.info(f"No video stream found for resolution: {format}")
                        return False, f"No stream found for resolution {format}"
                    ys.download(output_path=output_folder)
                    return title, output_file_path

                else:
                    logger.info("No valid stream found for the provided format")
                    return False, "Invalid format provided"
            except Exception as e:
                logger.error(e)
                return False, f"{e}"

            time.sleep(1)

    async def yts(keyword):
        try:
            logger.info("Searching...")
            result = Search(keyword).results
            logger.info(f"Video Found: {len(result)}")
            return result
        except Exception as e:
            logger.error(e)

    async def get_subtitles(url):
        for i in range(5):
            try:
                logger.info("Getting Subtitles...")
                yt = YouTube(url, po_token_verifier=PYTUBE.po, use_po_token=True)
                captions = yt.captions
                if captions:
                    lang_code = list(captions.lang_code_index.keys())[0]
                    print(lang_code)
                    subtitles = captions.get_by_language_code(lang_code).generate_srt_captions().split("\n")
                    print(subtitles[:10])
                    subtitles.insert(0, " ")
                    subtitle = " ".join([subtitles[i] for i in range(len(subtitles)) if i % 4 == 3])
                    return subtitle

                time.sleep(1)

            except:
                return False


