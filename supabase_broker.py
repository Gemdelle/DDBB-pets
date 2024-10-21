from supabase import create_client, Client
from nicegui import ui
import asyncio
import warnings

warnings.filterwarnings("ignore", message="coroutine 'AsyncServer.enter_room' was never awaited")


class SupabaseBroker:
    def __init__(self, url: str, key: str):
        self.supabase: Client = create_client(url, key)

    def fetch_data(self, view: str):
        try:
            response = self.supabase.table(view).select('*').execute()
            return response.data
        except Exception as e:
            print(f"Error fetching data: {str(e)}")
            return None


broker = SupabaseBroker('https://utinuuwlewcicllipaoc.supabase.co',
                        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV0aW51dXdsZXdjaWNsbGlwYW9jIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjcwOTQxNzcsImV4cCI6MjA0MjY3MDE3N30.b449FFa7ZXqFEFcGTx2Yo9SwknQWKXYrSZYiPhwX-ig')


async def load_data(view: str):
    data = broker.fetch_data(view)
    print(f"Fetched data: {data}")  # Debug output

    if data:
        columns = [{'label': col, 'field': col} for col in list(data[0].keys())]
        rows = [{col: str(value).replace('\n', '') for col, value in row.items()} for row in data]
        return columns, rows
    else:
        return None, None


async def update_table():
    print("Updating table...")
    loading_label.visible = True
    columns, rows = await load_data('view_mascota_detalle')
    loading_label.visible = False

    if columns and rows:
        table.columns = columns
        table.rows = rows
        ui.notify(f"Loaded {len(rows)} rows of data", color="green")
        print(f"Table updated with {len(rows)} rows")
    else:
        ui.notify('No data available or error occurred', color="orange")
        print("No data available or error occurred")


@ui.page('/')
def main():
    global table, loading_label


    ui.add_css('body { '
                'background-image: url("https://drive.google.com/thumbnail?id=1BRjmEroGeHaHgh6LbINNOeXsLs5kl95i&sz=w1000&format=png"); '
                'background-size: cover; '
                'background-position: center; '
                'background-repeat: no-repeat; '
                'height: 100vh; '
                'margin: 0; '
                '}')

    with ui.column().classes('w-full h-full items-center'):
        with ui.row().classes('w-full items-center'):
            ui.label('Pet Details Database').classes('text-2xl mb-4')


        with ui.row().classes('w-full').style('height: 500px; display: flex; flex-wrap: nowrap; overflow-x: scroll;'):

            for i in range(10):
                with ui.column().classes('flex items-center justify-center').style('''
                    width: 200px; 
                    height: 300px; 
                    background-color: blue; 
                    margin-right: 10px;
                    color: white;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                '''):
                    ui.label(f'Row {i+1}')
                    ui.label(f'Content {i+1}')



ui.run()
