from bot import logger
from pytubefix import YouTube
from pytubefix.cli import on_progress
from pytubefix import Search


class PYTUBE:
    async def ytdl(url, format: str = "720p", ):
        try:
            logger.info("Starting Download...")
            yt = YouTube(url, on_progress_callback=on_progress)
            title = yt.title
            output_folder = f"downloads"
            output_file_path = f"{output_folder}/{title}"
            
            if "kbps" in format:
                output_file_path+=".mp3"
                ys = yt.streams.filter(only_audio=True).get_by_resolution(format)
                ys.download(mp3=True, output_path=output_folder)
                return title, output_file_path
            elif "p" in format:
                output_file_path+=".mp4"
                logger.info(format)
                ys = yt.streams.get_by_resolution(format)
                ys.download(output_path=output_folder)
                return title, output_file_path
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

    async def get_resolutions(url):
        try:
            logger.info("Getting Resolutions...")
            yt = YouTube(url, on_progress_callback=on_progress)

            # Filter and remove duplicates while preserving order
            resolutions_mp4 = []
            for s in yt.streams.filter(file_extension="mp4").order_by("resolution"):
                if s.resolution not in resolutions_mp4:
                    resolutions_mp4.append(s.resolution)

            resolutions_mp3 = [s.abr for s in yt.streams.filter(only_audio=True) if s.abr]

            return {'mp4': resolutions_mp4, 'mp3': resolutions_mp3}
        except Exception as e:
            logger.error(e)


