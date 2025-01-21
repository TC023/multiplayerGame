import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from Player import Player
from random import randint
import requests
import sys
sys.path.append('..')


screen_width, screen_height = 900, 900

textures = []

filenames = ["./img/floor.png", "./img/grass.png", "./img/wall.png", "./img/creeper.png"]

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
    
    response = requests.get(f"{url}/send-data")
    
    if response.status_code == 200:
        response2 = response.json()
        # print("Datos de jugadores:", response.json())
        for player_id, player_data in response2["Players"].items():
            # print(f"Player ID: {player_id}, Position: {player_data['pos']}")    
            if player_id != id:
                # print(player_data["pos"], type(player_data["pos"]))
                cubo(*player_data["pos"])
    else:
        print("Failed to retrieve data:", response.text)
    

    
    pygame.display.flip()


pygame.init()
init()

done = False
clock = pygame.time.Clock()

id = str(randint(0,1_000))
print(id)
url = "https://7090f242-2f4d-4065-aa86-75bccd3b116b-00-e4x2ntccemiq.janeway.replit.dev"


while not done:
    display()
    yoSendThis = {
        "id": id,
        "pos": jugador.Position
    }
    requests.post(f"{url}/receive", json=yoSendThis)


    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            
    verX = jugador.Position[0] + jugador.newDir[0]
    verZ = jugador.Position[2] + jugador.newDir[2]
    if not jugador.especial:
        glLoadIdentity()
        gluLookAt(jugador.Position[0], jugador.Position[1], jugador.Position[2], verX, jugador.Position[1], verZ, 0, 1, 0)


    clock.tick(60)  # 60 FPS

pygame.quit()
