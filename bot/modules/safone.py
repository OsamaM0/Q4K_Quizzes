from bot import logger
from SafoneAPI import SafoneAPI
from g4f.client import Client


safone_api = SafoneAPI()
client = Client()

class Safone:
    async def safone_ai(msg):
        chatgpt_res = None
        bard_res = None
        chatbot_res = None
        try:
            chatgpt_res = await safone_api.chatgpt(msg)
        except Exception as e:
            logger.error(e)
            try:
                bard_res = await safone_api.bard(msg)
            except Exception as e:
                logger.error(e)
                try:
                    chatbot_res = await safone_api.chatbot(msg)
                except Exception as e:
                    logger.error(e)
        return chatgpt_res, bard_res, chatbot_res


    async def webshot(url):
        try:
            res = await safone_api.webshot(url)
            return res
        except Exception as e:
            logger.error(e)

    async def imagine(prompt):
        try:
            # Generate image using g4f client
            response = await client.images.async_generate(
                model="sdxl",
                prompt=prompt
                # Add any other necessary parameters
            )
            image_url = response.data[0].url
            print("IMAGE URL",image_url)
            return image_url
        except Exception as e:
            logger.error(e)

    # async def imagine(prompt):
    #     try:
    #         res = await safone_api.imagine(prompt)
    #         res = res[0]
    #         return res
    #     except Exception as e:
    #         logger.error(e)



# from bot import logger
# from g4f.client import Client
# import requests  # For direct webshot handling

# client = Client()

# class Safone:
#     async def safone_ai(msg):
#         chatgpt_res = None
#         bard_res = None
#         chatbot_res = None
#         try:
#             chatgpt_res = await client.chatgpt(msg)
#         except Exception as e:
#             logger.error(e)
#             try:
#                 bard_res = await client.bard(msg)
#             except Exception as e:
#                 logger.error(e)
#                 try:
#                     chatbot_res = await client.chatbot(msg)
#                 except Exception as e:
#                     logger.error(e)
#         return chatgpt_res, bard_res, chatbot_res

#     async def webshot(url):
#         try:
#             # Using an API service for webshot without browser drivers
#             # api_url = f"https://api.screenshotmachine.com?key=YOUR_API_KEY&url={url}&dimension=1024x768"
#             response = requests.get(api_url)
#             if response.status_code == 200:
#                 # Saving the screenshot to a file
#                 with open('webshot.png', 'wb') as f:
#                     f.write(response.content)
#                 return 'webshot.png'
#             else:
#                 logger.error(f"Webshot failed with status code {response.status_code}")
#         except Exception as e:
#             logger.error(e)

#     async def imagine(prompt):
#         try:
#             # Generate image using g4f client
#             response = client.images.generate(
#                 model="dall-e-3",
#                 prompt=prompt
#                 # Add any other necessary parameters
#             )
#             image_url = response.data[0].url
#             return image_url
#         except Exception as e:
#             logger.error(e)
