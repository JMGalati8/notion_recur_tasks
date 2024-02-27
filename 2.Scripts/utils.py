import os 
from dotenv import load_dotenv
from notion_client import Client
from datetime import datetime, timedelta, date


def update_db_rows(notion_client, db_row_ids):

    for id in db_row_ids:
        db_row = notion_client.pages.retrieve(page_id=id)
        due_date = datetime.fromisoformat(db_row['properties']['Due']['date']['start']).date()
        recur_interval = db_row['properties']['Recur Interval']['number']

        if date.today() > due_date:
            new_due_date = (due_date + timedelta(days=recur_interval)).isoformat()

            notion_client.pages.update(
                **{
                    'page_id':id,
                    'properties': {
                        'Due': {
                            'date': {'start': new_due_date}
                        },
                        'Done': {
                            'checkbox': False
                        }
                    }
                }
            )

        #print(db_row['properties']['Recur Interval']['number'].keys())


def update_db(notion_client, db_row_ids):
    db_rows = notion_client.databases.query(
        **{
            'database_id':db_id,
            'filter': {'property': 'Type', 'rich_text': {'contains': 'Recurring'}}
        }
    )

    for r in db_rows['results']:
        db_page_id = r['id']
        due_date = datetime.fromisoformat(r['properties']['Due_Date']['date']['start']).date()
        
        recur_interval = r['properties']['Recur Interval']['number']

        if date.today() > due_date:
            new_due_date = (due_date + timedelta(days=recur_interval)).isoformat()

            notion_client.pages.update(
                **{
                    'page_id':db_page_id,
                    'properties': {
                        'Due_Date': {
                            'date': {'start': new_due_date}
                        },
                        'Done': {
                            'checkbox': False
                        }
                    }
                }
            )


def get_page_info(notion_client, search_id):
    response = notion_client.blocks.children.list(block_id=search_id)

    for res in response['results']:
        child_db = res.get('child_database')
        child_page = res.get('child_page')

        if child_db:
            print(f"Title: {child_db['title']} | Type: Database | ID: {res['id'].replace('-','')}")

        if child_page:
            print(f"Title: {child_page['title']} | Type: Page | ID: {res['id'].replace('-','')}")



def return_db_rows(notion_client, search_id, print_info=False):
    response = notion_client.databases.query(
        **{
            'database_id':search_id,
            'filter': {'property': 'Type', 'formula': {'string': {'contains': 'Recurring'}}}
        }
    )    

    db_row_list = []
    for row in response['results']:
        clean_row_id = row['id'].replace('-','')
        db_row_list.append(clean_row_id)

        if print_info:
            print(f"Task Name: {row['properties']['Task']['title'][0]['text']['content']} | Task ID: {clean_row_id}")

    return db_row_list


    

# Split this into query_db & update_db
# Make a function to return all objects on the main page - So DBs and Pages, include their name, id and type