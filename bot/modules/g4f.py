import g4f
from bot import logger


class G4F:
    @staticmethod
    async def chatgpt(prompt):
        try:
            
            response = g4f.ChatCompletion.create(
                # model="gpt-3.5-turbo",
                model=g4f.models.gpt_4,
                messages=[{"role": "user", "content": prompt}]
            )
            return response
        except Exception as e:
            logger.error(e)

    @staticmethod
    async def imagine(prompt):
        try:
            response = g4f.images.generate(
                model="stability-ai/sdxl",
                prompt=prompt
            )
            image_url = response.data[0].url
            return image_url
        except Exception as e:
            logger.error(e)
