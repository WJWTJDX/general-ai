# Basic wrapper to start process with any game that has proper interface.

from __future__ import print_function
from __future__ import division

import os
import time

from games.alhambra import Alhambra
from games.torcs import Torcs
from games.mario import Mario
from games.game2048 import Game2048

loc = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
# prefix = Master directory
prefix = os.path.dirname(os.path.dirname(loc)) + "\\"  # cut two last directories

PYTHON_EXE = " \"C:\\Anaconda2\\envs\\py3k\\python.exe\""
PYTHON_SCRIPT = " \"" + prefix + "general-ai\\Controller\\script.py\""

MARIO = "java -cp \"" + prefix + "MarioAI\\MarioAI4J\\bin;" + prefix + "MarioAI\\MarioAI4J-Playground\\bin;" + prefix + "MarioAI\\MarioAI4J-Playground\\lib\\*\" mario.GeneralAgent"
GAME2048 = prefix + "2048\\2048\\bin\\Release\\2048.exe"
ALHAMBRA = prefix + "general-ai\\Game-interfaces\\Alhambra\\AlhambraInterface\\AlhambraInterface\\bin\\Release\\AlhambraInterface.exe"

TORCS = "\"" + prefix + "general-ai\\Game-interfaces\\TORCS\\torcs_starter.bat\""
TORCS_XML = " \"" + prefix + "general-ai\\Game-interfaces\\TORCS\\race_config.xml\""
TORCS_JAVA_CP = " \"" + prefix + "general-ai\\Game-interfaces\\TORCS\\scr-client\\classes;" + prefix + "general-ai\\Game-interfaces\\TORCS\\scr-client\\lib\\*\""
PORT = " \"3002\""
TORCS_EXE_DIRECTORY = " \"C:\\Users\\Jan\\Desktop\\torcs\""  # TODO: Relative path via cmd parameter
#TORCS_EXE_DIRECTORY = " \"C:\\Program Files (x86)\\torcs\"" # TODO: Relative path via cmd parameter

torcs_command = TORCS + TORCS_XML + TORCS_JAVA_CP + PORT + PYTHON_SCRIPT + TORCS_EXE_DIRECTORY + PYTHON_EXE
alhambra_command = ALHAMBRA + PYTHON_SCRIPT + PYTHON_EXE
game2048_command = GAME2048 + PYTHON_SCRIPT + PYTHON_EXE
mario_command = MARIO + PYTHON_SCRIPT + PYTHON_EXE


if __name__ == '__main__':

    model_config = " \"" + loc + "\\config\\random.json\""
    start = time.time()
    #game = Game2048(game2048_command + model_config)
    #game = Alhambra(alhambra_command + model_config)
    game = Torcs(torcs_command + model_config)
    #game = Mario(mario_command + model_config)



    """ SOME PARALLEL TESTING
    xml1 = " \"" + prefix + "general-ai\\Game-interfaces\\TORCS\\race_config_0.xml\""
    xml2 = " \"" + prefix + "general-ai\\Game-interfaces\\TORCS\\race_config_1.xml\""
    port1 = " \"3001\""
    port2 = " \"3002\""

    data = [(xml1, port1), (xml2, port2)]
    import concurrent.futures
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        for (xml, port) in data:
            torcs_command = TORCS + xml + TORCS_JAVA_CP + port + PYTHON_SCRIPT + TORCS_EXE_DIRECTORY + PYTHON_EXE
            print(torcs_command)
            game = Torcs(torcs_command + model_config)
            future = executor.submit(game.run)
            results.append(future)


    for i in range(len(results)):
        while not results[i].done():
            time.sleep(50)
        print(results[i].result())
    """

    print(game.run())
    end = time.time()
    print(end - start)
