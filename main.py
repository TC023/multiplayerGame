import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from Player import Player
from random import randint
import asyncio
import requests
import aiohttp

screen_width, screen_height = 790, 790

textures = []

filenames = ["./img/floor.png", "./img/grass.png", "./img/wall.png", "./img/creeper.png"]

# Your Player class and texture-loading function remain unchanged
jugador = Player()

def Texturas(filepath):
    textures.append(glGenTextures(1))
    id = len(textures) - 1
    glBindTexture(GL_TEXTURE_2D, textures[id])
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    image = pygame.image.load(filepath).convert()
    w, h = image.get_rect().size
    image_data = pygame.image.tostring(image, "RGBA")
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
    glGenerateMipmap(GL_TEXTURE_2D)


def init():
    """Initialize OpenGL for 3D rendering."""
    pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("OpenGL: 3D Simulation")
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, (screen_width / screen_height), 1, 1000.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(10, 10, 10, 0, 0, 0, 0, 1, 0)
    glEnable(GL_DEPTH_TEST)
    glClearColor(0, 0, 0, 0)
    for i in filenames:
        Texturas(i)

def cubo(x, y, z):
    # Se dibuja el cubo
    # ...
    glPushMatrix()
    glTranslate(x, y, z)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3d(1, 1, 1)
    glTexCoord2f(0.0, 1.0)
    glVertex3d(1, 1, -1)
    glTexCoord2f(1.0, 1.0)
    glVertex3d(1, -1, -1)
    glTexCoord2f(1.0, 0.0)
    glVertex3d(1, -1, 1)

    #2nd face
    glTexCoord2f(0.0, 0.0)
    glVertex3d(-1, 1, 1)
    glTexCoord2f(0.0, 1.0)
    glVertex3d(1, 1, 1)
    glTexCoord2f(1.0, 1.0)
    glVertex3d(1, -1, 1)
    glTexCoord2f(1.0, 0.0)
    glVertex3d(-1, -1, 1)

    #3rd face
    glTexCoord2f(0.0, 0.0)
    glVertex3d(-1, 1, -1)
    glTexCoord2f(0.0, 1.0)
    glVertex3d(-1, 1, 1)
    glTexCoord2f(1.0, 1.0)
    glVertex3d(-1, -1, 1)
    glTexCoord2f(1.0, 0.0)
    glVertex3d(-1, -1, -1)

    #4th face
    glTexCoord2f(0.0, 0.0)
    glVertex3d(1, 1, -1)
    glTexCoord2f(0.0, 1.0)
    glVertex3d(-1, 1, -1)
    glTexCoord2f(1.0, 1.0)
    glVertex3d(-1, -1, -1)
    glTexCoord2f(1.0, 0.0)
    glVertex3d(1, -1, -1)

    #top
    glTexCoord2f(0.0, 0.0)
    glVertex3d(1, 1, 1)
    glTexCoord2f(0.0, 1.0)
    glVertex3d(-1, 1, 1)
    glTexCoord2f(1.0, 1.0)
    glVertex3d(-1, 1, -1)
    glTexCoord2f(1.0, 0.0)
    glVertex3d(1, 1, -1)

    glEnd()
    glPopMatrix()

def piso():
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textures[1])  # Use the first texture
    glColor3f(0.278, 0.804,  0.200)
    glBegin(GL_QUADS)
    
    glTexCoord2f(0.0, 0.0)
    glVertex3d(-100, -1, -100)

    glTexCoord2f(0.0, 100)
    glVertex3d(100, -1, -100)

    glTexCoord2f(100, 100)
    glVertex3d(100, -1, 100)
    
    glTexCoord2f(100, 0.0)
    glVertex3d(-100, -1, 100)
    glEnd()
    glDisable(GL_TEXTURE_2D)

def display():
    """Render all objects."""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    piso()
    cubo(0, 0, 0)
    jugador.update()
    pygame.display.flip()

async def fetch_player_data(session, url):
    """Fetch data from the server asynchronously."""
    try:
        async with session.get(f"{url}/send-data") as response:
            if response.status == 200:
                return await response.json()
            print("Failed to retrieve data:", await response.text())
    except Exception as e:
        print(f"Error fetching player data: {e}")
    return None


player_id = str(randint(0, 1_000))

async def send_player_data(url):
    """Send player data to the server asynchronously."""
    try:
        yoSendThis = {
            "id": player_id,
            "pos": jugador.Position
        }
        # await asyncio.get_event_loop().run_in_executor(None, requests.post, f"{url}/receive",yoSendThis) 
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{url}/receive", json=yoSendThis) as response:
                return await response.text()
        # print(lol.json())

    except Exception as e:
        print(f"Error sending player data: {e}")

async def periodic_update(url):
    # print("periodic")
    while True:
        response = await send_player_data(url)
        # print(response)
        
        await asyncio.sleep(0.1)

url = "https://7090f242-2f4d-4065-aa86-75bccd3b116b-00-e4x2ntccemiq.janeway.replit.dev"
pygame.init()
init()

async def game_loop():
    """Main game loop with asynchronous networking."""
    asyncio.create_task(periodic_update(url))
    done = False
    clock = pygame.time.Clock()

    while not done:
        # Render and update game
        display()
        # await send_player_data(session, url, player_data)
        # await asyncio.get_event_loop().run_in_executor(None, requests.get, f"{url}/recieve")

        # server_data = await fetch_player_data(session, url)
        # if server_data:
        #     for other_id, other_player in server_data["Players"].items():
        #         if other_id != player_id:
        #             cubo(*other_player["pos"])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # Camera view
        verX = jugador.Position[0] + jugador.newDir[0]
        verZ = jugador.Position[2] + jugador.newDir[2]
        if not jugador.especial:
            glLoadIdentity()
            gluLookAt(jugador.Position[0], jugador.Position[1], jugador.Position[2], 
                        verX, jugador.Position[1], verZ, 0, 1, 0)

        await asyncio.sleep(0)
        clock.tick(60)  # 60 FPS

    pygame.quit()

asyncio.run(game_loop())
