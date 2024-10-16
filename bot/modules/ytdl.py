from bot import logger
from pytubefix import YouTube
from pytubefix.cli import on_progress
from pytubefix import Search


class PYTUBE:
    async def ytdl(url, extension: str = "mp4"):
        try:
            logger.info("Starting Download...")
            yt = YouTube(url, on_progress_callback=on_progress)
            title = yt.title
            ys = yt.streams.get_highest_resolution()

            if extension == "mp4":
                ys.download()
                return title, f"file_path/{yt.title}.mp4"
            elif extension == "mp3":
                ys.download(mp3=True)
                return title, f"file_path/{yt.title}.mp3"
            else:
                logger.info("No stream found for this video")
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
