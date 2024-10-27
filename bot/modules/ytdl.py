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
    @classmethod
    async def get_proxy_dict(cls):
        proxies = [
        "64.137.42.112:5157:ieakrmtg:9k7k5i3m9jsv",
        "167.160.180.203:6754:ieakrmtg:9k7k5i3m9jsv",
        "154.36.110.199:6853:ieakrmtg:9k7k5i3m9jsv",
        "173.0.9.70:5653:ieakrmtg:9k7k5i3m9jsv",
        "173.0.9.209:5792:ieakrmtg:9k7k5i3m9jsv"
        ]

        proxy = random.choice(proxies)
        ip, port, user, password = proxy.split(':')
        return {
            "http": f"socks5://{user}:{password}@{ip}:{port}",
            "https": f"socks5://{user}:{password}@{ip}:{port}"
        }

    async def ytdl(url, extention: str = "mp4"):
        for i in range(5):
            try:
                logger.info("Starting Download...")
                proxy_dict = await PYTUBE.get_proxy_dict()
                yt = YouTube(url, proxies=proxy_dict, on_progress_callback=on_progress)
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

    async def yts(keyword):
        try:
            logger.info("Searching...")
            result = Search(keyword).results
            logger.info(f"Video Found: {len(result)}")
            return result
        except Exception as e:
            logger.error(e)

    async def get_subtitles(url):
        try:
            for i in range(5):
                logger.info("Getting Subtitles...")
                proxy_dict = await PYTUBE.get_proxy_dict()
                yt = YouTube(url, proxies=proxy_dict)
                captions = yt.captions
                if captions:
                    lang_code = list(captions.lang_code_index.keys())[0]
                    print(lang_code)
                    subtitles = captions.get_by_language_code(lang_code).generate_srt_captions().split("\n")
                    print(subtitles[:10])
                    subtitles.insert(0, " ")
                    subtitle = " ".join([subtitles[i] for i in range(len(subtitles)) if i % 4 == 3])
                    return subtitle

                time.sleep(5)


        except:
            return False


