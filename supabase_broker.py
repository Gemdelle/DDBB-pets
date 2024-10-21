from supabase import create_client, Client
from nicegui import ui
import asyncio
import warnings

warnings.filterwarnings(
    "ignore", message="coroutine 'AsyncServer.enter_room' was never awaited")


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
        columns = [{'label': col, 'field': col}
                   for col in list(data[0].keys())]
        rows = [{col: str(value).replace('\n', '')
                 for col, value in row.items()} for row in data]
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

    ui.add_css('''    
        body {
            background-image: url("https://drive.google.com/thumbnail?id=1NoLgwKw_wqB7kbtcBBigVNlxZ3Xbqj3A&sz=w1000&format=png");
            background-size: 100% 100%;
            background-position: center;
            background-repeat: no-repeat;
            height: 100vh;
            margin: 0;
            overflow: hidden;
            font-family: 'Georgia', serif;
        }
        .header {
            background-image: url("https://drive.google.com/thumbnail?id=1rq1WFWfhi17QR-G8k-Mx3gh-6CMgZvVg&sz=w1000&format=png");
            background-size: contain;
            background-position: center;
            background-repeat: no-repeat;
            height: 16vh;
            width: 10vw;
            margin: 0 auto;
            margin-top: 4vh;
            margin-bottom: 0;
        }
        .nav {
            width: 30vw;
            height: 4vw;
            display: flex;
            flex-direction: row;
            justify-content: space-between;
            align-items: center;
            font-size: 2vh;
            margin-top: 0;
            color: #777355;
        }
        .nav-button {
            width: 30%;
            height: 100%;
            cursor: pointer;
            transition: transform 0.3s ease-in-ease-out;
            background-size: contain;
            background-repeat: no-repeat;
            background-image: url(" https://drive.google.com/thumbnail?id=1fnXmKmLMcoMN9k9OIrcSzComyw6fPCSb&sz=w1000&format=png");
            background-position: center;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .nav-button:hover {
            scale: 105%;
        }
        .pet-card.bone-blue {
            background-image: url("https://drive.google.com/thumbnail?id=1r7G9R_RmQemob-sWqJzAJjbQlcLYdQcf&sz=w1000&format=png");
            background-position: center;
            background-repeat: no-repeat;
            background-size: contain;
        }
        .pet-card.bone-pink {
            background-image: url("https://drive.google.com/thumbnail?id=16hd19sOhwTH7qk2VvFDQLLkpwMgtAg_A&sz=w1000&format=png");
        }
        .pet-card.bone-yellow {
            background-image: url("https://drive.google.com/thumbnail?id=1fnXmKmLMcoMN9k9OIrcSzComyw6fPCSb&sz=w1000&format=png");
        }
        .paw-number {
            width: 50px;
            height: 50px;
            background-image: url("https://drive.google.com/thumbnail?id=1hyQfKd1gq_naMGoxw_Gp1ceLEBM8eubI&sz=w1000&format=png");
            background-size: contain;
            background-repeat: no-repeat;
            position: absolute;
            top: 10px;
            left: 10px;
            display: flex;
            justify-content: center;
            align-items: center;
            padding-top: 10%;
            color: #474533;
        }
        .description {
            background-color: #D3ECD7;
            border: 5px solid #5CDAE1;
            width: 90%;
            height: 53%;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 2vh 2vh !important;
            color: #474533;
        }
        .bone-name {
            background-color: #FFC0CB;
            border-radius: 20px;
            padding: 5px 15px;
            font-weight: bold;
            margin-bottom: 15px;
            color: #474533;
        }
        .title-container {
            width: 15vw;
            height: 10vh;
            background-size: contain;
            background-repeat: no-repeat;
            background-image: url(" https://drive.google.com/thumbnail?id=1fnXmKmLMcoMN9k9OIrcSzComyw6fPCSb&sz=w1000&format=png");
            background-position: center;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 3vh;
            color: #474533;
        }
        .overflow-x-auto {
            overflow-x: auto;  /* Habilita el desplazamiento horizontal */
            white-space: nowrap;  /* Evita que los elementos se ajusten a una nueva línea */
        }
        .pet-img {
            width: 80%;
            height: 50%;
            position: absolute;
            top: 0;
            background-size: contain;
            background-repeat: no-repeat;
            background-image: url("https://drive.google.com/thumbnail?id=1rYGlNaM67-TTWrBl-6wOEBcftcl0LSsb&sz=w1000&format=png");
            background-position: center;
        }
        .container {
            display: flex;
            justify-content: center;
            height: 49vh;
        }
        .pet-card {
            margin: 1%;
            position: relative;
            width: 28vh;
            height: 95%;
            border-radius: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-end;
        }
    ''')

    with ui.column().classes('w-full h-full items-center'):
        with ui.row().classes():
            ui.row().classes('header')  # Logo URL

        with ui.row().classes('nav'):
            with ui.column().classes('nav-button home-circle').on('click', lambda: ui.open('/mascotas')):
                ui.label('M a s c o t a s')  # Hueso Azul como fondo
            with ui.column().classes('nav-button home-circle').on('click', lambda: ui.open('/interesados')):
                ui.label('I n t e r e s a d o s')  # Hueso Amarillo como fondo
            with ui.column().classes('nav-button home-circle').on('click', lambda: ui.open('/veterinaria')):
                ui.label('V e t e r i n a r i a')  # Hueso Rosado como fondo

        with ui.row().classes('title-container'):
            ui.label('M A S C O T A S')

        with ui.row().classes('container overflow-x-auto'):
            # Carta de la mascota 1
            with ui.column().classes('pet-card'):
                with ui.column().classes('pet-img'):
                    ui.label('12').classes('paw-number')  # Número en la patita
                
                
                with ui.column().classes('description'):

                    ui.label('Animal: Perro')
                    ui.label('Pelaje: Corto')
                    ui.label('Estado: Rescatado')
                    ui.label('Temperamento: Amistoso')
                    ui.label('Treat: Comida')
                    ui.label('Comida: Ración')

            with ui.column().classes('pet-card bone-blue'):
                ui.label('12').classes('paw-number')  # Número en la patita
                with ui.label('Lala').classes('bone-name'):  # Nombre en el hueso rosa central
                    pass
                with ui.column().classes('description'):
                    ui.label('Animal: Perro')
                    ui.label('Pelaje: Corto')
                    ui.label('Estado: Rescatado')
                    ui.label('Temperamento: Amistoso')
                    ui.label('Treat: Comida')
                    ui.label('Comida: Ración')

            with ui.column().classes('pet-card bone-blue'):
                ui.label('12').classes('paw-number')  # Número en la patita
                with ui.label('Lala').classes('bone-name'):  # Nombre en el hueso rosa central
                    pass
                with ui.column().classes('description'):
                    ui.label('Animal: Perro')
                    ui.label('Pelaje: Corto')
                    ui.label('Estado: Rescatado')
                    ui.label('Temperamento: Amistoso')
                    ui.label('Treat: Comida')
                    ui.label('Comida: Ración')

            with ui.column().classes('pet-card bone-blue'):
                ui.label('12').classes('paw-number')  # Número en la patita
                with ui.label('Lala').classes('bone-name'):  # Nombre en el hueso rosa central
                    pass
                with ui.column().classes('description'):
                    ui.label('Animal: Perro')
                    ui.label('Pelaje: Corto')
                    ui.label('Estado: Rescatado')
                    ui.label('Temperamento: Amistoso')
                    ui.label('Treat: Comida')
                    ui.label('Comida: Ración')                
            
            with ui.column().classes('pet-card bone-blue'):
                ui.label('12').classes('paw-number')  # Número en la patita
                with ui.label('Lala').classes('bone-name'):  # Nombre en el hueso rosa central
                    pass
                with ui.column().classes('description'):
                    ui.label('Animal: Perro')
                    ui.label('Pelaje: Corto')
                    ui.label('Estado: Rescatado')
                    ui.label('Temperamento: Amistoso')
                    ui.label('Treat: Comida')
                    ui.label('Comida: Ración')

            with ui.column().classes('pet-card bone-blue'):
                ui.label('12').classes('paw-number')  # Número en la patita
                with ui.label('Lala').classes('bone-name'):  # Nombre en el hueso rosa central
                    pass
                with ui.column().classes('description'):
                    ui.label('Animal: Perro')
                    ui.label('Pelaje: Corto')
                    ui.label('Estado: Rescatado')
                    ui.label('Temperamento: Amistoso')
                    ui.label('Treat: Comida')
                    ui.label('Comida: Ración')

            with ui.column().classes('pet-card bone-blue'):
                ui.label('12').classes('paw-number')  # Número en la patita
                with ui.label('Lala').classes('bone-name'):  # Nombre en el hueso rosa central
                    pass
                with ui.column().classes('description'):
                    ui.label('Animal: Perro')
                    ui.label('Pelaje: Corto')
                    ui.label('Estado: Rescatado')
                    ui.label('Temperamento: Amistoso')
                    ui.label('Treat: Comida')
                    ui.label('Comida: Ración')

ui.run()

