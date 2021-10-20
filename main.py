import pygame as py
lineCol = [251, 197, 49]
scrW = 1600
scrH = 900
running = True
pressing = False
pointsX = []
pointsY = []

py.init()
img = py.image.load("fll2.bmp")
screen = py.display.set_mode((scrW, scrH))
py.display.set_caption('KepLErGO Editor')
bckgrnd = py.Surface((800, 450))
screen.blit(img, (0, 0))
while running:
    
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
    if py.mouse.get_pressed(3)[0] and not pressing:
        py.draw.circle(screen, lineCol,py.mouse.get_pos(), 10)
        pressing = True
        pointsX.append(py.mouse.get_pos()[0])
        pointsY.append(py.mouse.get_pos()[1])
        if len(pointsX) > 1:
            py.draw.line(screen, lineCol, (pointsX[len(pointsX) - 1], pointsY[len(pointsY) - 1] ), (pointsX[len(pointsX) - 2], pointsY[len(pointsY) - 2]))
    elif not py.mouse.get_pressed(3)[0]:
        pressing = False
    py.display.flip()

py.quit()