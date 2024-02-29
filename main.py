import pandas as pd
import os 
from dotenv import load_dotenv
from notion_client import Client
import utils


def main():
    load_dotenv()
    notion_client = Client(auth=os.environ["NOTION_API_KEY"])

    # Returns all blocks on notion 
    utils.get_page_info(notion_client=notion_client, search_id=os.environ['NOTION_HEAD_PAGE_ID'])

    db_list = utils.return_db_rows(notion_client=notion_client, search_id=os.environ['NOTION_TASK_DB_ID'], print_info=True)

    utils.update_db_rows(notion_client=notion_client, db_row_ids=db_list)


if __name__ == "__main__":
    main()


