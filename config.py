from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv('TOKEN')
GROUP = os.getenv('GROUP')
ADMIN = int(os.getenv('ADMIN'))
