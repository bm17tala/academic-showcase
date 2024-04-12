import pygame
import pysine
import threading
from random import randint 
import sort_visualize
import os

WIDTH = 854
HEIGHT = 480
TITLE = "Academic Showcase"

BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)

frequency = 0


#testArray = [ randint(0, HEIGHT) for i in range(600) ]

def runGUI(testArray):
    global frequency

    onScreenArr = []

    for i in testArray:
        onScreenArr.append(int(i.data*100000))


    max = onScreenArr[0]
    for i in range(1, len(onScreenArr)):
        if onScreenArr[i] > max:
            max = onScreenArr[i]

    min = onScreenArr[0]
    for i in range(1, len(onScreenArr)):
        if onScreenArr[i] < min:
            min = onScreenArr[i]

    heightRatio = (max - min) / HEIGHT 

    barWidth = WIDTH / len(onScreenArr)

    pygame.init()

    screen = pygame.display.set_mode( (WIDTH, HEIGHT), pygame.RESIZABLE )
    

    

    pygame.display.set_caption(TITLE)

    clock = pygame.time.Clock()

    posLock = threading.Lock()
    t1 = threading.Thread(target=sort_visualize.quickSort, args=[onScreenArr, 0, len(onScreenArr) - 1, posLock])
    t1.start()


    soundLock = threading.Lock()
    soundThread = threading.Thread(target=playSound, args=[])
    soundThread.start()


    while True:
        
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                pygame.quit()
                os._exit(0)

        
                
        currentHeight = screen.get_height()
        currentWidth = screen.get_width()

        if len(onScreenArr) > currentWidth:
            newOnScreenArr = average_of_chunks(onScreenArr, int(len(onScreenArr) / currentWidth))
        else:
            newOnScreenArr = onScreenArr

        heightRatio = (max - min) / currentHeight
        if len(onScreenArr) > currentWidth:
            barWidth = 1
        else:
            barWidth = currentWidth / len(newOnScreenArr)
        


        screen.fill(BLACK)

        


        # print(currentHeight - onScreenArr[i] * 1/heightRatio)
        print(len(newOnScreenArr))
        for i in range(len(newOnScreenArr)):
            with posLock:
                if i == int(sort_visualize.currentPos1  / int(len(onScreenArr) / currentWidth)) or i == int(sort_visualize.currentPos2  / int(len(onScreenArr) / currentWidth)):

                        
                    pygame.draw.rect(screen, RED, [ i*barWidth, currentHeight - (newOnScreenArr[i]-min) * 1/heightRatio,
                                                        barWidth, ( (newOnScreenArr[i]-min) * 1/heightRatio)],0)
                        
                    with soundLock:
                        frequency = ((newOnScreenArr[i]-min) * 1/heightRatio) + 500
                        
                        
                        
                else:
                    pygame.draw.rect(screen, GREEN, [ i*barWidth, currentHeight - (newOnScreenArr[i]-min) * 1/heightRatio,
                                                        barWidth, ( (newOnScreenArr[i]-min) * 1/heightRatio)],0)
                    
                
        pygame.display.update()

        
            
            
        clock.tick(60)

def playSound():
    global frequency

    while sort_visualize.sorting:
        pysine.sine(frequency=frequency, duration=0.05) 

def average_of_chunks(arr, chunk_size):
    averages = []
    for i in range(0, len(arr), chunk_size):
        chunk = arr[i:i+chunk_size]
        average = sum(chunk) / len(chunk)
        averages.append(average)
    return averages
