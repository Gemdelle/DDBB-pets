from supabase import create_client, Client
from nicegui import ui
import asyncio
import warnings

warnings.filterwarnings(
    "ignore", message="coroutine 'AsyncServer.enter_room' was never awaited")


class SupabaseBroker:
    def __init__(self, url: str, key: str):
        self.supabase: Client = create_client(url, key)

    async def fetch_data(self, view: str):
        try:
            response = self.supabase.table(view).select('*').execute()
            return response.data
        except Exception as e:
            print(f"Error fetching data: {str(e)}")
            return None


broker = SupabaseBroker(
    'https://utinuuwlewcicllipaoc.supabase.co',
    'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV0aW51dXdsZXdjaWNsbGlwYW9jIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjcwOTQxNzcsImV4cCI6MjA0MjY3MDE3N30.b449FFa7ZXqFEFcGTx2Yo9SwknQWKXYrSZYiPhwX-ig'
)


def create_pet_card(pet_data):
    if pet_data["genero"] == "Macho":
        paw_number_class = 'paw-number-blue'
        description_class = 'description-blue'
        bone_class = 'bone-blue'
    else:
        paw_number_class = 'paw-number-pink'
        description_class = 'description-pink'
        bone_class = 'bone-pink'

    with ui.column().classes('pet-card'):
        with ui.column().classes('pet-photo-container'):
            photo_style = f'background-image: url({pet_data["foto"]});' if pet_data.get("foto") else ''
            ui.column().classes('pet-photo').style(photo_style)
            ui.column().classes('pet-img')
            ui.label(str(pet_data.get('dias_estadia', ''))).classes(paw_number_class)

        with ui.column().classes(description_class):
            with ui.column().classes(f'pet-card {bone_class}'):
                ui.label(pet_data['nombre_mascota'])
            ui.label(f'Animal: {pet_data["animal"]}').classes('description-text')
            ui.label(f'Estado: {pet_data["estado"]}').classes('description-text')
            ui.label(f'Temperamento: {pet_data["temperamento"]}').classes('description-text')
            ui.label(f'Treat: {pet_data["treat"]}').classes('description-text')
            ui.label(f'Comida: {pet_data["comida"]}').classes('description-text')
            ui.label(f'Ración: {pet_data["racion_kg"]} kg').classes('description-text')
            ui.label(f'Peso: {pet_data["peso"]} kg').classes('description-text')
            ui.label(f'Género: {pet_data["genero"]}').classes('description-text')

def create_header_nav():
    with ui.row().classes():
        ui.row().classes('header')

    with ui.row().classes('nav'):
        with ui.column().classes('nav-button home-circle').on('click', lambda: ui.navigate.to('/')):
            ui.label('M a s c o t a s')
        with ui.column().classes('nav-button home-circle').on('click', lambda: ui.navigate.to('/interesados')):
            ui.label('I n t e r e s a d o s')
        with ui.column().classes('nav-button home-circle').on('click', lambda: ui.navigate.to('/veterinaria')):
            ui.label('V e t e r i n a r i a')


@ui.page('/')
async def main():
    ui.add_css(common_css + additional_css)

    with ui.column().classes('w-full h-full items-center no-gap'):
        create_header_nav()

        with ui.row().classes('title-container'):
            ui.label('M A S C O T A S').classes('page-title')

        with ui.row().classes('container overflow-x-auto'):
            pet_data = await broker.fetch_data('view_mascota_detalle')
            if pet_data:
                for pet in pet_data:
                    create_pet_card(pet)
            else:
                ui.label('No hay mascotas disponibles').classes('text-lg text-gray-500')


@ui.page('/interesados')
async def interesados_page():
    ui.add_css(common_css + additional_css)

    with ui.column().classes('w-full h-full items-center no-gap'):
        create_header_nav()

        with ui.row().classes('title-container'):
            ui.label('I N T E R E S A D O S').classes('page-title')

        with ui.row().classes('container overflow-x-auto'):
            pet_data = await broker.fetch_data('view_interesados')
            if pet_data:
                for pet in pet_data:
                    create_pet_card(pet)
            else:
                ui.label('No hay mascotas disponibles').classes('text-lg text-gray-500')


def create_veterinaria_pet_card(pet_data):
    if pet_data.get("genero") == "Macho":
        paw_number_class = 'paw-number-blue'
        description_class = 'description-blue'
        bone_class = 'bone-blue'
    else:
        paw_number_class = 'paw-number-pink'
        description_class = 'description-pink'
        bone_class = 'bone-pink'

    with ui.column().classes('pet-card'):
        with ui.column().classes('pet-photo-container'):
            photo_style = f'background-image: url({pet_data["foto"]});' if pet_data.get("foto") else ''
            ui.column().classes('pet-photo').style(photo_style)

            vaccine_style = f'background-image: url({pet_data["imagen_vacuna"]});' if pet_data.get("imagen_vacuna") else ''
            ui.column().classes(paw_number_class).style(vaccine_style)

        with ui.column().classes(description_class + ' description-vaccine'):
            with ui.column().classes(f'pet-card {bone_class}'):
                ui.label(pet_data.get('nombre_mascota', 'Unknown Pet'))

            ui.label(f'Animal: {pet_data.get("animal", "Unknown")}').classes('description-text')
            ui.label(f'Peso: {pet_data.get("estado", "N/A")}').classes('description-text')
            ui.label(f'Estado: {pet_data.get("temperamento", "N/A")}').classes('description-text')
            ui.label(f'Id vacuna: {pet_data.get("treat", "N/A")}').classes('description-text')
            ui.label(f'Nombre vacuna: {pet_data.get("comida", "N/A")}').classes('description-text')
            ui.label(f'Fecha vacunación: {pet_data.get("racion_kg", "0")} kg').classes('description-text')

        ui.column().classes('pet-card vaccine')


@ui.page('/veterinaria')
async def veterinaria_page():
    ui.add_css(common_css + additional_css)

    with ui.column().classes('w-full h-full items-center no-gap'):
        create_header_nav()

        with ui.row().classes('title-container'):
            ui.label('V E T E R I N A R I A').classes('page-title')

        with ui.row().classes('container overflow-x-auto'):
            pet_data = await broker.fetch_data('vista_historial_medico')
            if pet_data:
                for pet in pet_data:
                    create_veterinaria_pet_card(pet)
            else:
                ui.label('No hay mascotas disponibles').classes('text-lg text-gray-500')


additional_css = '''
    .pet-card.bone-yellow {
        background-image: url("https://drive.google.com/thumbnail?id=1fnXmKmLMcoMN9k9OIrcSzComyw6fPCSb&sz=w1000&format=png");
        background-position: center;
        background-repeat: no-repeat;
        background-size: contain;
        display: flex;
        justify-content: center;
        align-items: center;
        text-transform: uppercase;
    }

    .pet-card.bone-pink {
        background-image: url("https://drive.google.com/thumbnail?id=16hd19sOhwTH7qk2VvFDQLLkpwMgtAg_A&sz=w1000&format=png");
        background-position: center;
        background-repeat: no-repeat;
        background-size: contain;
        display: flex;
        justify-content: center;
        align-items: center;
        text-transform: uppercase;
        position: absolute;
        top: -3vh;
        height: 7vh;
        width: 18vh;
        z-index: 100;
    }
    .pet-card.vaccine {
        background-image: url("https://drive.google.com/thumbnail?id=1i7EqVspmhDu35i-8M_qt65s-ErtIMbFW&sz=w1000&format=png");
        background-position: center;
        background-repeat: no-repeat;
        background-size: contain;
        display: flex;
        justify-content: center;
        align-items: center;
        position: absolute;
        bottom: -3vh;
        right: -2vh;
        height: 9vh;
        width: 9vh;
        z-index: 100;
    }
'''

common_css = '''    
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
            margin-top: 7vh;
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
            display:flex;
            justify-content: center;
            align-items: center;
            text-transform: uppercase;
            position: absolute;
            top: -3vh;
            height: 7vh;
            width: 18vh;
            z-index: 100;
        }
        .pet-card.bone-pink {
            background-image: url("https://drive.google.com/thumbnail?id=16hd19sOhwTH7qk2VvFDQLLkpwMgtAg_A&sz=w1000&format=png");
        }
        .pet-card.bone-yellow {
            background-image: url("https://drive.google.com/thumbnail?id=1fnXmKmLMcoMN9k9OIrcSzComyw6fPCSb&sz=w1000&format=png");
        }
        .paw-number-blue {
            width: 8vh;
            height: 8vh;
            background-image: url("https://drive.google.com/thumbnail?id=1hyQfKd1gq_naMGoxw_Gp1ceLEBM8eubI&sz=w1000&format=png");
            background-size: contain;
            background-repeat: no-repeat;
            position: absolute;
            top: 0;
            left: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            padding-top: 10%;
            color: #474533;
            font-size: 2.5vh;
            z-index: 100;
        }
        .paw-number-pink {
            width: 8vh;
            height: 8vh;
            background-image: url("https://drive.google.com/thumbnail?id=1UcwqAisO684D-ZK4Bv9J0bHKc8vwB2sz&sz=w1000&format=png");
            background-size: contain;
            background-repeat: no-repeat;
            position: absolute;
            top: 0;
            left: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            padding-top: 10%;
            color: #474533;
            font-size: 2.5vh;
            z-index: 100;
        }
        .description-blue {
            background-color: #D3ECD7;
            border: 5px solid #5CDAE1;
            width: 90%;
            height: 60%;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: flex-end;
            gap: unset;
            padding: 3vh 2vh 1vh 2vh !important;
            color: #474533;
            position: relative;
        }
        .description-pink {
            background-color: #FBF7D2;
            border: 5px solid #F7C1D8;
            width: 90%;
            height: 60%;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: flex-end;
            gap: unset;
            padding: 3vh 2vh 1vh 2vh !important;
            color: #474533;
            position: relative;
        }
        .description-text {
            font-size: 1.4vh;
        }
        .description-vaccine { 
            justify-content: center;
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
            width: 100%;
                height: 100%;
                position: absolute;
                top: 0;
                background-size: 100% 100%;
                background-repeat: no-repeat;
                background-image: url("https://drive.google.com/thumbnail?id=1iVJXodlKPDRGEbRbwMMlmJI1yprGCNfL&sz=w1000&format=png");
            background-position: center;
            z-index: 99;
        }
        .pet-photo {
            background-size: 100% 100%;
                background-repeat: no-repeat;
                background-image: url("https://lh3.googleusercontent.com/d/1_UBEmmBTTvt4mihRm-BevaqYvmFu2mt-=w1000?authuser=0");
                background-position: center;
                border-radius: 50%;
                width: 80%;
                height: 80%;
            margin: 0 auto;
            margin-top: 2vh;
            z-index: 1;
        }
        .pet-photo-container {
            width: 80%;
            height: 60%;
            top: 4vh;
            position: relative;
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
            .page-title {
                font-size: 2.2vh;
            }
            .no-gap {
                gap: unset;
            }
        '''

ui.run()
