# coding=utf-8
import json
import time
import datetime
import shutil

json_filename = "./records/record_list.json"

record_list = []

ISOTIMEFORMAT = '%Y-%m-%d %H.%M.%S'

def on_load(server, old):
    global record_list
    monitor(server)

def saveJson():
    with open(json_filename, 'w') as f:
        json.dump(record_list, f, indent=4)

def monitor(server):
    theTime = datetime.datetime.now().strftime(ISOTIMEFORMAT)
    shutil.copy(json_filename, './records/' + str(theTime) + '.json')
    PI = server.get_plugin_instance('PlayerInfoAPI')
    OP = server.get_plugin_instance('OnlinePlayerAPI')
    while True:
        players = OP.get_player_list()
        for i in range(len(players)):
            try:
                pos = PI.getPlayerInfo(server, players[i], path='Pos')
            except:
                continue
            try:
                x = int(pos[0])
            except:
                x = "Error"
            try:
                y = int(pos[1])
            except:
                y = "Error"
            try:
                z = int(pos[2])
            except:
                z = "Error"
            try:
                dim = PI.getPlayerInfo(server, players[i], path='Dimension')
            except:
                continue
            if dim == -1:
                dim = "Nether"
            elif dim == 0:
                dim = "World"
            elif dim == 1:
                dim = "End"
            theTime = datetime.datetime.now().strftime(ISOTIMEFORMAT)
            info = str(theTime) + " " + str(players[i]) + " " + str(dim) + " x:" + str(x)+ " y:" + str(y)+ " z:" + str(z)
            record_list.append(info)
            saveJson()
        time.sleep(12)