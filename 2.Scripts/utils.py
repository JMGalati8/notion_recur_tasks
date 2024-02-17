import os 
from dotenv import load_dotenv
from notion_client import Client
from datetime import datetime, timedelta, date


def update_db(db_id, notion_client):
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

# Split this into query_db & update_db
# Make a function to return all objects on the main page - So DBs and Pages, include their name, id and type