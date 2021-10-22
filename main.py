import pygame as py

lineCol = [251, 197, 49]
scrW = 1000
scrH = 700
running = True
pressing = False
pointsX = []
pointsY = []
circleSize = 10
circlesX = []
circlesY = []

py.init()

def render():
    screen.blit(img, (0, 0))
    if len(circlesX) > 0:
        for lol in range(0, len(circlesX)):
            py.draw.circle(screen, (0, 0, 255), (circlesX[lol], circlesY[lol]), circleSize)
        for i in range(0, len(circlesX) - 1):
            py.draw.aaline(screen, (0, 125, 255), (circlesX[i], circlesY[i]), (circlesX[i + 1], circlesY[i + 1]))
    py.display.flip()
 

img = py.image.load("fll2.bmp")
screen = py.display.set_mode((scrW, scrH))
py.display.set_caption('KepLErGO Editor')
bckgrnd = py.Surface((800, 450))
while running:
    
    for event in py.event.get():
        if event.type == py.KEYDOWN:
            if event.key == py.K_z:
                try:
                    circlesX.pop()
                    circlesY.pop()
                except:
                    print("You cannot destroy objects that dont exist!")
        if event.type == py.QUIT:
            running = False
    if py.mouse.get_pressed(3)[0] and not pressing:
        py.draw.circle(screen, lineCol,py.mouse.get_pos(), circleSize)
        pressing = True
        pointsX.append(py.mouse.get_pos()[0])
        pointsY.append(py.mouse.get_pos()[1])
        circlesX.append(py.mouse.get_pos()[0])
        circlesY.append(py.mouse.get_pos()[1])
        if len(pointsX) > 1:
            py.draw.aaline(screen, lineCol, (pointsX[len(pointsX) - 1], pointsY[len(pointsY) - 1] ), (pointsX[len(pointsX) - 2], pointsY[len(pointsY) - 2]))
    elif not py.mouse.get_pressed(3)[0]:
        pressing = False
    if py.mouse.get_pressed(3)[2]:
        for i in range(0, len(pointsX)):
            if(py.mouse.get_pos()[0] > pointsX[i] - 5 and py.mouse.get_pos()[0] < pointsX[i] + 5):
                if(py.mouse.get_pos()[1] > pointsY[i] - 5 and py.mouse.get_pos()[1] < pointsY[i] + 5):
                    rect1 = py.Rect(py.mouse.get_pos()[0], py.mouse.get_pos()[1], 50, 200)
            i = i + 1
    render()

py.quit()