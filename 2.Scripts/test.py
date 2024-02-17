import pandas as pd
import os 
from dotenv import load_dotenv
from notion_client import Client
from datetime import datetime, timedelta, date 
import json
import utils

    
if __name__ == "__main__":
    load_dotenv()

    notion_client = Client(auth=os.environ["NOTION_API_KEY"])

    utils.update_db(db_id=os.environ['NOTION_TEST_DB_ID'], notion_client=notion_client)

    