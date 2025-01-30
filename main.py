import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from Player import Player
from random import randint
import asyncio
import requests
import aiohttp

screen_width, screen_height = 750, 750

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

serverData = {
    "players": {}  # Use lowercase "players" to match WebSocket updates
}

async def websocket_listener(url):
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(f"{url}/ws") as ws:
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    global serverData
                    print(serverData)
                    serverData = msg.json()

async def send_updates(url):
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(f"{url}/ws") as ws:
            while True:
                await ws.send_json({
                    "update": {
                        "id": player_id,
                        "pos": jugador.Position
                    }
                })
                await asyncio.sleep(0.05)  # 20 updates/sec

import time
player_states = {}  # Track player positions and timestamps

def interpolate_position(player_id, new_pos):
    now = time.time()
    if player_id not in player_states:
        player_states[player_id] = {
            "pos": new_pos,
            "timestamp": now
        }
        return new_pos
    
    old_state = player_states[player_id]
    elapsed = now - old_state["timestamp"]
    
    # Linear interpolation (adjust factor based on your tick rate)
    interpolated = [
        old + (new - old) * min(elapsed * 20, 1.0)  # 20 updates/sec
        for old, new in zip(old_state["pos"], new_pos)
    ]
    
    player_states[player_id] = {
        "pos": new_pos,
        "timestamp": now
    }
    return interpolated


def display():
    global serverData

    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    piso()
    cubo(0, 0, 0)
    jugador.update()
    # print(serverData)
    
    for server_player_id, player_data in serverData["players"].items():
        if server_player_id != player_id:
            # Store previous position and timestamp for interpolation
            current_pos = player_data["pos"]
            # Render with interpolated position
            interpolated_pos = interpolate_position(server_player_id, current_pos)
            cubo(*interpolated_pos)
    pygame.display.flip()

player_id = str(randint(0, 1_000))

url = "http://127.0.0.1:5000"
pygame.init()
init()

async def game_loop():
    """Main game loop with asynchronous networking."""
    # asyncio.create_task(periodic_update(url))
    asyncio.create_task(websocket_listener(url))
    asyncio.create_task(send_updates(url))
    done = False
    clock = pygame.time.Clock()

    while not done:
        # Render and update game
        display()
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
