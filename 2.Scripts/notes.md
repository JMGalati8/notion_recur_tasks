

### Pages are blocks - Treat them the same way to get all their children
page_block_results = notion.blocks.children.list(block_id=page_id)  
- This will give a list of all the blocks within this page under the 'results' key  
- Each child is represented in its own dictionary

### Getting DB info
notion.databases.retrieve will retrieve the db object (cols, properties and other) but not the rows.  
notion.databases.query gets db rows  
When filtering - Use 'rich_text' for text. No I don't know why the notion_client and notion docs both say something different either.

### Creating Info
notion.pages.create will create new pages (rows in db). The properties seems weird as you can't pass in the properties of the DB as far I found  
You just give it what properties you want to fill out, and then also say what you want to use in those properties.



def create_page():
    create_response = notion.pages.create(
        parent= {
            'type': 'database_id',
            'database_id': os.environ['NOTION_TEST_DB_ID']
        },
        properties={
            'Name': {'title': [{'text': {'content': 'Test Task 4 - Tags'}}]},
            'Tags': {'type': 'multi_select', 'multi_select': [{'name': 'First'}]}
        }
    )

    return create_response


if __name__ == "__main__":
    load_dotenv()

    notion = Client(auth=os.environ["NOTION_API_KEY"])

    query_results = notion.search(query='Integration')
    db_id = query_results['results'][0]['id']
    
    page_results = notion.pages.retrieve(page_id=db_id)
    #print(page_results)
    
    page_block_results = notion.blocks.children.list(block_id=db_id)
    ez_db_id = page_block_results.get('results')[0]['id']

    ez_db_response = notion.databases.retrieve(database_id=ez_db_id)
    db_properties = ez_db_response.get('properties')
    db_rows = notion.databases.query(
        **{
            'database_id':ez_db_id,
            'filter': {'property': 'Type', 'rich_text': {'contains': 'Recurring'}}
        }
    )

    #print(db_rows['results'][0]['properties']['Recur Interval'])
    print(db_rows['results'][0]['id'])
    db_page_id = db_rows['results'][0]['id']
    print(db_rows['results'][0]['properties']['Recur Interval']['number'])
    print(type(db_rows['results'][0]['properties']['Recur Interval']['number']))
    new_date = db_rows['results'][0]['properties']['Due_Date']['date']['start']
    new_date_date = datetime.fromisoformat(new_date) + timedelta(days=2)
    print(type(new_date_date))
    print(new_date_date.date())
    #print( json.dumps(new_date_date.date()))
    update_date = new_date_date.date().isoformat()
    print(update_date)
    print(type(update_date))
    page_update_response = notion.pages.update(
        **{
            'page_id':db_page_id,
            'properties': {
                'Next_Due_Date': {
                    'date': {'start': update_date}
                }
            }
        }
    )

    # Next Steps - Fix all of this
    # For each response in the query, get the due date and the recur interval. Create new due date, then If today > due_date, set due_date to the next due date. Enter next due date into that column as well.
    # Make that a function too.
    # Fix all of how we get there too

    #create_response = create_page()