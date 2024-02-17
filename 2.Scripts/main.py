import pandas as pd
import os 
from dotenv import load_dotenv
from notion_client import Client
from u


if __name__ == "__main__":
    load_dotenv()

    notion = Client(auth=os.environ["NOTION_API_KEY"])


