# coding=utf-8
import json
import time
import datetime
import shutil

sleep = 12

fp_x = 0
fp_y = 0
fp_z = 0

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
        try:
            for i in range(len(players)):
                pos = PI.getPlayerInfo(server, players[i], path='Pos')
                x = int(pos[0])
                y = int(pos[1])
                z = int(pos[2])
                dim = PI.getPlayerInfo(server, players[i], path='Dimension')
                pre = " 危 "
                if fp_x-50<=x<=fp_x+50 and fp_z-50<z<fp_z+50 and fp_y-10<=y<=fp_y+10 and dim==-1:
                    server.say("§c"+ "Warning!" + pre + players[i] + pre + "在伪和平传送门附近游荡！！！")
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
        except:
            continue
        time.sleep(sleep)