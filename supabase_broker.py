from supabase import create_client, Client
from nicegui import ui
import warnings

warnings.filterwarnings("ignore", message="coroutine 'AsyncServer.enter_room' was never awaited")

class SupabaseBroker:
    def __init__(self, url: str, key: str):
        self.supabase: Client = create_client(url, key)

    def fetch_data(self, table: str):
        # This assumes the response is not async, and you need to access .data
        response = self.supabase.table(table).select('*').execute()
        return response.data  # Accessing 'data' correctly as an attribute


# Replace these with your actual Supabase URL and Key
broker = SupabaseBroker('https://utinuuwlewcicllipaoc.supabase.co', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV0aW51dXdsZXdjaWNsbGlwYW9jIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjcwOTQxNzcsImV4cCI6MjA0MjY3MDE3N30.b449FFa7ZXqFEFcGTx2Yo9SwknQWKXYrSZYiPhwX-ig')


async def load_data():
    data = broker.fetch_data('raza')

    # Extract column names and clean up the rows
    if data:
        columns = list(data[0].keys())
        rows = [[str(value).replace('\n', '') for value in row.values()] for row in data]

        # Create table with specified columns and rows
        if rows:
            ui.table(columns=columns, rows=rows).style('width: 80%; margin: 0 auto;')
        else:
            ui.notify('No data available')
    else:
        ui.notify('No data available')


# Create a centered layout
with ui.column().style('align-items: center; justify-content: center; height: 100vh;'):
    ui.button('Load Data', on_click=load_data)
    ui.element('div').style('height: 20px')  # Small spacing between button and table

# Start the NiceGUI server
ui.run()
