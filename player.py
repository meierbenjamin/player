# -*- coding: utf-8 -*-
import pygame
import RPi.GPIO as GPIO
import sys
import time
import os

pygame.mixer.init()

def playSound( song ):
    print( 'Play {}'.format( song ) )
    #pygame.mixer.music.fadeout( 300 )
    pygame.mixer.music.load( './music/{}'.format( song ) )
    pygame.mixer.music.play()

abort = False

music = [
    { "sw": [0, 0, 0, 1], "song": '01 - Trybguet.mp3' },
    { "sw": [0, 0, 1, 0], "song": '02 - Schlangenäscht.mp3' },
    { "sw": [0, 1, 0, 0], "song": '11 - Compañero.mp3' },
    { "sw": [1, 0, 0, 0], "song": '03 - Brandschtifter.mp3' },
    { "sw": [0, 0, 1, 1], "song": 'Mini Farb und dini.mp3' },
    { "sw": [0, 1, 0, 1], "song": 'Zoge am Bogä _ Meiteli wenn du witt go tanzä.mp3' },
    { "sw": [1, 0, 0, 1], "song": 'Siebe chugelrundi Säu _ Kinderlieder by ChinderMusigWält (128kbit_AAC) (online-audio-converter.com).mp3' },
    { "sw": [0, 1, 1, 0], "song": 'S Ramseiers wei go grase.mp3' },
    { "sw": [1, 0, 1, 0], "song": 'Hoppe, hoppe Reiter.mp3' },
    { "sw": [1, 1, 0, 0], "song": 'Patent Ochsner - Für immer uf di.mp3' },
    { "sw": [0, 1, 1, 1], "song": 'Farbenfrohe Lieder.mp3' },
    { "sw": [1, 0, 1, 1], "song": 'Patent Ochsner - Guet Nacht, Elisabeth.mp3' }
]

def trigger( states, levels ):
    valid = True
    levels = map( lambda lvl: True if lvl == 1 else False, levels )
    for i, state in enumerate( states ):
        if levels[ i ] != states[ i ]:
            valid = False
    return valid
                             
def selectSound( states, music ):
    for sound in music:
        if trigger( states, sound[ 'sw' ] ):
            return sound[ 'song' ]
    return None

def play():
    global abort
    global music
    GPIO.setmode( GPIO.BCM )
    GPIO.setup( 21, GPIO.IN, pull_up_down=GPIO.PUD_UP )

    io = [ 21, 20, 26, 19 ]

    for i in io:
        GPIO.setup( i, GPIO.IN, pull_up_down=GPIO.PUD_UP )

    states = map( lambda i: False, io )

    print( states )

    state = False
    #while pygame.mixer.music.get_busy() == True:
    while not abort:
        time.sleep( 0.05 )
        for x, i in enumerate( io ):
            if not states[ x ]:
                if not GPIO.input( i ):
                    states[ x ] = True
                    #print( 'Positive edge {i}'.format( i = i ) )
                    sng = selectSound( states, music )
                    if sng:
                        playSound( sng )
            else:
                if GPIO.input( i ):
                    #print( 'Negative edge {i}'.format( i = i ) )
                    states[ x ] = False
                    #pygame.mixer.music.stop()
                    #abort = True
        continue

    pygame.mixer.music.stop()

if __name__ == '__main__':
    try:
        play()
    except KeyboardInterrupt:
        print( 'Shutdown' )
        abort = True
        try:
            sys.exit( 0 )
        except SystemExit:
            os._exit( 0 )
