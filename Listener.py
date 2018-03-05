import argparse
import math

from pythonosc import dispatcher
from pythonosc import osc_server

import numpy as np
from numpy import *

from graphics import *

import threading
import time

win = None
bar = None

# Constants
past500samples = [0 for _ in range(501)]     # Updated every time we get a new value
concentrationLevel = 0

concentrationLevelsList = []


def eeg_handler(unused_addr, args, ch1, ch2, ch3, ch4):
    global concentrationLevel
    global past500samples

    # Remove first element, add current EEG value to end of list
    past500samples.pop(1)
    past500samples.append(ch1)

    samplesThisBatch = past500samples[0]

    samplesThisBatch += 1

    #print(samplesThisBatch)

    if samplesThisBatch == 50:
        samplesThisBatch = 0

        # Convert to numPy array
        reals = np.array(past500samples[1:])
        
        fftResult = [abs(x) for x in np.fft.rfft(reals)]    # abs to get rid of complex nums

        concentrationLevel = 0
        for i in range(10,30):
            concentrationLevel += fftResult[i]
        
        concentrationLevel /= 3500
        concentrationLevelsList.append(concentrationLevel)

    past500samples[0] = samplesThisBatch

    f = open('output.txt', 'w+')
    for value in concentrationLevelsList:
        f.write(str(value) + '\n')
    f.close()


args = None

def server():
    global args

    _dispatcher = dispatcher.Dispatcher()
    _dispatcher.map("/debug", print)
    _dispatcher.map("/muse/eeg", eeg_handler, "EEG")

    server = osc_server.ThreadingOSCUDPServer(
        (args.ip, args.port), _dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()

def main():
    global win
    global bar
    global args

    print('Starting')

    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
                        default="127.0.0.1",
                        help="The ip to listen on")
    parser.add_argument("--port",
                        type=int,
                        default=5001,
                        help="The port to listen on")
    args = parser.parse_args()
    
    serverThread = threading.Thread(target=server)
    serverThread.start()

    win = GraphWin('Output', 1000, 100)
    win.setCoords(0, 0, 100, 10)

    bar = Rectangle(Point(1, 1), Point(9, 9))
    bar.setFill('white')
    bar.draw(win)

    while True:
        bar = Rectangle(Point(round(concentrationLevel),1), Point(99,9))
        bar.setFill('white')
        bar.draw(win)

        bar = Rectangle(Point(1, 1), Point(round(concentrationLevel), 9))

        if concentrationLevel < 15:
            bar.setFill('green')
        elif concentrationLevel < 40:
            bar.setFill('blue')
        else:
            bar.setFill('red')

        bar.draw(win)

        #* Draw threshold bars
        bar = Rectangle(Point(15, 0), Point(15.1, 10))
        bar.setFill('black')
        bar.draw(win)

        bar = Rectangle(Point(40, 0), Point(40.1, 10))
        bar.draw(win)

        time.sleep(0.001)

if __name__ == '__main__':
    main()