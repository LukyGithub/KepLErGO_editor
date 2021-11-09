import pygame as py
from math import sqrt

MainCol = [155, 89, 182] #Color paletete
SubCol = [50, 0, 80]
MenuCol = [52, 152, 219]
TextCol = [0, 0, 0]
transparent = [0, 0, 0, 0]

scrW = 1456 #Sizes
scrH = 1008
menuWidth = 200
menuHeight = 300
fontSize = 24

running = True #Variables
pressing = False
circleSize = 10
circlesX = []
circlesY = []
rectangle = []
texts = []
lineSpacing = 25
activeDot = 0
manualAdd = False
manualType = ""
robotSpeed = 10
py.init()

def render():
    screen.blit(img, (0, 0))
    if len(circlesX) > 0:
        for lol in range(0, len(circlesX)):
            py.draw.circle(screen, MainCol, (circlesX[lol], circlesY[lol]), circleSize)
        for i in range(0, len(circlesX) - 1):
            py.draw.aaline(screen, MainCol, (circlesX[i], circlesY[i]), (circlesX[i + 1], circlesY[i + 1]))

            calculated = [0, 0, 0, 0, 0]
            calculated[0] = (circlesX[i] + circlesX[i + 1]) /2
            calculated[1] = (circlesY[i] + circlesY[i + 1]) /2
            calculated[2] = circlesX[i] - circlesX[i + 1]
            calculated[3] = circlesY[i] - circlesY[i + 1]
            calculated[4] = sqrt(calculated[2]**2 + calculated[3]**2)
            lineText = font.render(str(round(calculated[4])), True, SubCol)
            if calculated[2] > 0 or calculated[3] > 0:
                if calculated[0] > calculated[1]:
                    lineRect = (calculated[0], calculated[1] + 25)
                else:
                    lineRect = (calculated[0] + 25, calculated[1])
            else:
                if calculated[0] < calculated[1]:
                    lineRect = (calculated[0], calculated[1])
                else:
                    lineRect = (calculated[0] - 25, calculated[1])
            screen.blit(lineText, lineRect)

        if len(rectangle) > 0:
            getrect = py.Rect(rectangle[0], rectangle[1], menuWidth, menuHeight)
            py.draw.rect(screen, MenuCol, getrect)
            splits = ""
            if len(texts) >= activeDot + 1:
                splits = texts[activeDot].split('/')
            else:
                while len(texts) - 1 < activeDot:
                    texts.append("")
                splits = texts[activeDot].split('/')
            text = []
            textRect = []
            for i in range(0, len(splits)):
                try:
                    text[i] = font.render(splits[i], True, TextCol)
                    textRect[i] = text[i].get_rect()
                except:
                    text.append(font.render(splits[i], True, TextCol))
                    textRect.append(text[i].get_rect())
                xpos = rectangle[0] + 5
                textRect[i] = (xpos , rectangle[1] + lineSpacing * i)
                screen.blit(text[i], textRect[i])
        if manualAdd:
            newrect = py.Rect(scrW / 2, scrH / 2, 200, 50)
            py.draw.rect(screen, MenuCol, newrect)
            manualText = font.render(manualType, True, TextCol)
            manualRect = (scrW / 2, scrH / 2)
            screen.blit(manualText, manualRect)
                

    py.display.flip()

img = py.image.load("fll2.bmp")
img = py.transform.scale(img, (1456, 1008))
screen = py.display.set_mode((scrW, scrH), py.RESIZABLE)
py.display.set_caption('KepLErGO Editor')
bckgrnd = py.Surface((800, 450))
font = py.font.Font('Roboto-Regular.ttf', fontSize)
icon = py.image.load("icon.bmp")
py.display.set_icon(icon)

while running:
    for event in py.event.get():
        if event.type == py.KEYDOWN:
            if len(rectangle) > 1:
                if event.key == py.K_BACKSPACE:
                    texts[activeDot] = texts[activeDot][:-1]
                elif event.key == py.K_RETURN:
                    texts[activeDot] += '/'
                else:
                    texts[activeDot] += event.unicode
            elif  manualAdd:
                if event.key == py.K_BACKSPACE:
                    manualType = manualType[:-1]
                elif event.key == py.K_RETURN:
                    splices = manualType.split(', ')
                    circlesX.append(int(splices[0]))
                    circlesY.append(int(splices[1]))
                    manualAdd = False
                else:
                    manualType += event.unicode
            else:
                if event.key == py.K_z:
                    try:
                        circlesX.pop()
                        circlesY.pop()
                    except:
                        print("You cannot destroy objects that dont exist!")
                if event.key == py.K_p:
                    print(texts)
                if event.key == py.K_a:
                    manualType = ""
                    manualAdd = True
        if event.type == py.QUIT:
            running = False

    if py.mouse.get_pressed(3)[0] and not pressing:
        py.draw.circle(screen, MainCol,py.mouse.get_pos(), circleSize)
        pressing = True
        circlesX.append(py.mouse.get_pos()[0])
        circlesY.append(py.mouse.get_pos()[1])
        if len(circlesX) > 1:
            py.draw.aaline(screen, MainCol, (circlesX[len(circlesX) - 1], circlesY[len(circlesY) - 1] ), (circlesX[len(circlesX) - 2], circlesY[len(circlesY) - 2]))
    if py.mouse.get_pressed(3)[2] and not pressing and len(rectangle) < 1:
        pressing = True
        for i in range(0, len(circlesX)):
            if(py.mouse.get_pos()[0] > circlesX[i] - 5 and py.mouse.get_pos()[0] < circlesX[i] + 5):
                if(py.mouse.get_pos()[1] > circlesY[i] - 5 and py.mouse.get_pos()[1] < circlesY[i] + 5):
                    activeDot = i
                    rectangle.append(py.mouse.get_pos()[0])
                    rectangle.append(py.mouse.get_pos()[1])
    elif py.mouse.get_pressed(3)[2] and not pressing and len(rectangle) > 1:
        pressing = True
        rectangle.pop()
        rectangle.pop()
    elif not py.mouse.get_pressed(3)[0] and not py.mouse.get_pressed(3)[2]:
        pressing = False
    render()

py.quit()