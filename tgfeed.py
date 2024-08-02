import asyncio
import logging
from telegram import Bot

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


class TGFeeds:
    def __init__(self,channel_id,bot_token) -> None:
        self.channel_id = channel_id
        self.bot_token = bot_token
        self.bot = Bot(token=bot_token)

    def post_image_message(self, entry):
        
        feed = {
            "title":      entry.get('info'),
            "page_date":  entry.get('page_date'),
            "image_url":  entry.get('image_url')
        }
        
        caption = f"""
                    <b>New Results Published on {feed['page_date']}</b> \n\n{feed['title']}
                """
                
        # Send a photo by providing a URL
        asyncio.run(self.bot.send_photo(chat_id=self.channel_id, photo=feed['image_url'],caption=caption,parse_mode='html'))
