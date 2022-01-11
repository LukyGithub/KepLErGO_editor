import pygame as py
import time
import tkinter
import tkinter.filedialog
from math import sqrt
from math import fabs


MainCol = [155, 89, 182] #Color paletete
SubCol = [50, 0, 80]
layerCol = [(26, 188, 15), (52, 152, 219), (155, 89, 182), (241, 196, 15), (231, 76, 60), (230, 126, 34), (46, 204, 113)]
MenuCol = [52, 152, 219]
TextCol = [0, 0, 0]
transparent = [0, 0, 0, 0]

scrW = 1456 #SizesposA[0] + GetPosition(1, dir)[0]
scrH = 1008
menuWidth = 200
menuHeight = 300
fontSize = 24

#Variables
running = True 
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
showLines = False
showPos = False
currentLayer = 0
layerDetails = []
editmode = False
moving = [False, 0]
newline = True
togglePreview = False
previewAngle = 0
robotRotated = None

py.init()
#print(open("editableTest.txt", 'r').read())
def createDir():
    top = tkinter.Tk()
    top.withdraw()
    fileName = tkinter.filedialog.asksaveasfilename(parent = top, filetypes=(("Text files", "*.txt"), ("Prolog files", "*.pl *.pro"), ("All files", "*.*")))
    top.destroy()
    return(fileName)

def chooseDir():
    top = tkinter.Tk()
    top.withdraw()
    fileName = tkinter.filedialog.askopenfilename(parent = top, filetypes=(("Text files", "*.txt"), ("Prolog files", "*.pl *.pro"), ("All files", "*.*")))
    top.destroy()
    return(fileName)

def export():
    try:
        fileDir = open(createDir(), "w")
        print(fileDir)
        fileDir.write(texts[0] + "\n")
        for i in range(1, len(circlesX)):
            while len(texts) - 1 < i:
                texts.append("")
            #x = (x-109)/5.32 y = abs(y-777)/5.32
            fileDir.write("goto(" + str(round((circlesX[i-1] - 109) / 5.32, 2)) + ", " + str(round(fabs(circlesY[i-1] - 777) / 5.32, 2)) + ", " + str(round((circlesX[i] - 109) / 5.32, 2)) + ", " + str(round(fabs(circlesY[i] - 777) / 5.32, 2)) + ")\n")
            fileDir.write(texts[i] + "\n")
        fileDir.write("#" + str(layerDetails))
    except:
        print("An unexpected error ocured")

def load(directory):
    global layerDetails
    global newline
    for i in range(0, len(circlesX)):
        try:
            circlesX.pop()
            circlesY.pop()
            texts.pop()
        except Exception as e:
            print("Some error occured whilst deleting existing points: " + str(e))
    textLine = open(directory, 'r')
    textLines = textLine.read().split("\n")
    print(textLines)
    for i in range(0, len(textLines)-1):
        #x = (x-109)/5.32 y = abs(y-777)/5.32
        localLine = textLines[i]
        if len(localLine) > 0:
            if localLine[0] == 'g':
                newline = True
                subsplit = textLines[i].replace("goto(", "")
                subsplit = subsplit.replace(")", "")
                subsplit = subsplit.split(", ")
                subsplit[0] = float(subsplit[0]) * 5.32 + 109
                subsplit[1] = -(float(subsplit[1]) * 5.32) + 777
                subsplit[2] = float(subsplit[2]) * 5.32 + 109
                subsplit[3] = -(float(subsplit[3]) * 5.32) + 777
                if i == 1:
                    circlesX.append(round(subsplit[0], 2))
                    circlesY.append(round(subsplit[1], 2))
                circlesX.append(round(subsplit[2], 2))
                circlesY.append(round(subsplit[3], 2))
                print(i)
                print(circlesX[:])
                print(circlesY[:])
            else:
                if newline:
                    texts.append(textLines[i])
                    newline = False
                else:
                    texts[-1] += "\n" + textLines[i] 
        else:
            texts.append("")
    for i in range(0, len(layerDetails)):
        layerDetails.pop()
    layerDetails = loadLayers(textLines[-1])
    print(layerDetails)
        
def loadLayers(text):
    layerint = text.replace("#[", "")
    layerint = layerint.replace("]]", "]")
    layerint = layerint.split("], ")
    for i  in range(0, len(layerint)):
        layerint[i] = layerint[i].replace("[", '')
        layerint[i] = layerint[i].split(", ")
        for b in range(0, len(layerint[i])):
            try:
                layerint[i][b] =int(layerint[i][b])
            except:
                layerint[i][b] = None
    return(layerint)

def render():
    screen.blit(img, (0, 0))
    layerText = bigFont.render("layer = " + str(currentLayer) + "/6", True, layerCol[0])
    escMode = bigFont.render(", Edit= " + str(editmode), True, layerCol[0])
    screen.blit(layerText, (600, 105))
    screen.blit(escMode, (825, 105))
    if togglePreview:
        screen.blit(robotRotated, (py.mouse.get_pos()[0]-40, py.mouse.get_pos()[1]-92))  
    if len(circlesX) > 0:
        if len(layerDetails[currentLayer]) > 0 or len(layerDetails[currentLayer - 1]) > 0:
    
            if currentLayer > 0:
                try:
                    for lol in range(layerDetails[currentLayer - 1][-1], layerDetails[currentLayer][-1] + 1):
                        py.draw.circle(screen, layerCol[currentLayer], (circlesX[lol], circlesY[lol]), circleSize)
                    for i in range(layerDetails[currentLayer -1][-1], layerDetails[currentLayer][-1]):
                        py.draw.aaline(screen,  layerCol[currentLayer], (circlesX[i], circlesY[i]), (circlesX[i + 1], circlesY[i + 1]))
                except:
                    py.draw.circle(screen, layerCol[currentLayer], (circlesX[layerDetails[currentLayer-1][-1]], circlesY[layerDetails[currentLayer-1][-1]]), circleSize)
            else:
                for lol in range(0, layerDetails[currentLayer][-1] +1):
                    py.draw.circle(screen, layerCol[currentLayer], (circlesX[lol], circlesY[lol]), circleSize)
                for i in range(layerDetails[currentLayer][0], layerDetails[currentLayer][-1]):
                    py.draw.aaline(screen, layerCol[currentLayer], (circlesX[i], circlesY[i]), (circlesX[i + 1], circlesY[i + 1]))


                    calculated = [0, 0, 0, 0, 0]
                    calculated[0] = (circlesX[i] + circlesX[i + 1]) /2
                    calculated[1] = (circlesY[i] + circlesY[i + 1]) /2
                    calculated[2] = circlesX[i] - circlesX[i + 1]
                    calculated[3] = circlesY[i] - circlesY[i + 1]
                    calculated[4] = sqrt(calculated[2]**2 + calculated[3]**2)
                    lineText = font.render(str(round(calculated[4] / 5.32, 2)), True, SubCol)
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
                    if showLines:
                        screen.blit(lineText, lineRect)

        if len(rectangle) > 0:
            getrect = py.Rect(rectangle[0], rectangle[1], menuWidth, menuHeight)
            py.draw.rect(screen, MenuCol, getrect)
            splits = ""
            if len(texts) >= activeDot + 1:
                splits = texts[activeDot].split('\n')
            else:
                while len(texts) - 1 < activeDot:
                    texts.append("")
                splits = texts[activeDot].split('\n')
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
        if showPos:
            for i in range(0, len(circlesX) - 1):
                posText = font.render(str(round(circlesX[i])) + ", " + str(round(circlesY[i])), True, SubCol)
                screen.blit(posText, (circlesX[i], circlesY[i] - 10))
    if manualAdd:
        newrect = py.Rect(scrW / 2, scrH / 2, 200, 50)
        py.draw.rect(screen, MenuCol, newrect)
        manualText = font.render(manualType, True, TextCol)
        manualRect = (scrW / 2, scrH / 2)
        screen.blit(manualText, manualRect)                  
    py.time.Clock().tick(60)
    py.display.flip()

#Do before the program starts
img = py.image.load("fll2.bmp")
img = py.transform.scale(img, (1456, 1008))

screen = py.display.set_mode((scrW, scrH), py.RESIZABLE)
py.display.set_caption('KepLErGO Editor')
bckgrnd = py.Surface((800, 450))
font = py.font.Font('Roboto-Regular.ttf', fontSize)
bigFont = py.font.Font('Roboto-Regular.ttf', 45)
icon = py.image.load("icon.bmp")
py.display.set_icon(icon)
robot1 = py.image.load("cropped_robot_nobg2.bmp")
robot1 = py.transform.scale(robot1, (81, 141))
for i in range(0, 10):
    layerDetails.append([])
robotRotated = py.transform.rotate(robot1, previewAngle)

while running:
    for event in py.event.get():
        if event.type == py.KEYDOWN:
            if len(rectangle) > 1:
                if event.key == py.K_BACKSPACE:
                    texts[activeDot] = texts[activeDot][:-1]
                elif event.key == py.K_RETURN:
                    texts[activeDot] += '\n'
                else:
                    texts[activeDot] += event.unicode
                    texts[activeDot] = texts[activeDot].replace("Goto", "goto")
                    texts[activeDot] = texts[activeDot].replace("GoTo", "goto")
                    print(texts[activeDot])
            elif  manualAdd:
                if event.key == py.K_BACKSPACE:
                    manualType = manualType[:-1]
                elif event.key == py.K_RETURN:
                    splices = manualType.split(', ')
                    circlesX.append((int(splices[0]) * 5.32) + 109)
                    circlesY.append(fabs(int(splices[1]) * 5.32 - 777))
                    layerDetails[currentLayer].append(len(circlesX)-1)
                    manualAdd = False
                else:
                    manualType += event.unicode
            else:
                if event.key == py.K_z:
                    try:
                        circlesX.pop()
                        circlesY.pop()
                        layerDetails[currentLayer].pop()
                    except:
                        print("You cannot destroy objects that dont exist!")
                if event.key == py.K_p:
                    showPos = not showPos
                if event.key == py.K_o:
                    print(str(circlesX) + ", " + str(circlesY))
                if event.key == py.K_a:
                    manualType = ""
                    manualAdd = True
        if event.type == py.KEYUP:
            if not manualAdd and not len(rectangle) > 1:
                if event.key == py.K_ESCAPE:
                    editmode = not editmode
                if event.key == py.K_UP:
                    if currentLayer < 6: 
                        currentLayer += 1
                if event.key == py.K_DOWN:
                    if currentLayer > 0:
                        currentLayer -= 1
                if event.key == py.K_e:
                    export()
                if event.key == py.K_l:
                    showLines = not showLines
                if event.key == py.K_c and not pressing and len(rectangle) < 1:
                    pressing = True
                    for i in range(0, len(circlesX)):
                        if(py.mouse.get_pos()[0] > circlesX[i] - 5 and py.mouse.get_pos()[0] < circlesX[i] + 5):
                            if(py.mouse.get_pos()[1] > circlesY[i] - 5 and py.mouse.get_pos()[1] < circlesY[i] + 5):
                                activeDot = i
                                rectangle.append(py.mouse.get_pos()[0])
                                rectangle.append(py.mouse.get_pos()[1])
                if event.key == py.K_m:
                    load(chooseDir())
                if event.key == py.K_t:
                    togglePreview = not togglePreview
                if event.key == py.K_RIGHT:
                    previewAngle -= 5
                    robotRotated = py.transform.rotate(robot1, previewAngle)
                if event.key == py.K_LEFT:
                    previewAngle += 5
                    robotRotated = py.transform.rotate(robot1, previewAngle)
        if event.type == py.QUIT:
            running = False

    if py.mouse.get_pressed(3)[0] and not pressing:
        if editmode:
            pressing = True
            if moving[0]:
                moving[0] = False
                circlesX[moving[1]] = py.mouse.get_pos()[0]
                circlesY[moving[1]] = py.mouse.get_pos()[1]
            else:
                for i in range(0, len(circlesX)):
                    if(py.mouse.get_pos()[0] > circlesX[i] - circleSize and py.mouse.get_pos()[0] < circlesX[i] + circleSize):
                        if(py.mouse.get_pos()[1] > circlesY[i] - circleSize and py.mouse.get_pos()[1] < circlesY[i] + circleSize):
                            moving[0] = True
                            moving[1] = i
        else:
            py.draw.circle(screen, MainCol,py.mouse.get_pos(), circleSize)
            pressing = True
            circlesX.append(py.mouse.get_pos()[0])
            circlesY.append(py.mouse.get_pos()[1])
            layerDetails[currentLayer].append(len(circlesX)-1)
    if py.mouse.get_pressed(3)[2] and not pressing and len(rectangle) < 1:
        pressing = True
        for i in range(0, len(circlesX)):
            if(py.mouse.get_pos()[0] > circlesX[i] - circleSize and py.mouse.get_pos()[0] < circlesX[i] + circleSize):
                if(py.mouse.get_pos()[1] > circlesY[i] - circleSize and py.mouse.get_pos()[1] < circlesY[i] + circleSize):
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