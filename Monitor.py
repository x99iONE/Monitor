# coding=utf-8
import json
import time
import datetime
import shutil
import re
import os

sleep = 10

json_filename = "./records/record_list.json"
site_info = "./config/site.json"
records = "./records

bot_list = []
record_list = []
site_list = {}

help_msg = '''----------- §aMCDR 监控插件帮助信息 §f-----------
§b!!mr help §f- §c显示帮助消息
§b!!mr add [坐标名] [x] [y] [z] [次元] §f- §c次元：world nether end
§b!!mr list §f- §c显示所有已有监控
§b!!mr reload §f- §c重载监控坐标，联系管理员删除后操作该指令
§e为防止随意删除更改监控点，删除监控请联系管理，玩家仅有添加权限
-----------------Monitor-----------------'''

ISOTIMEFORMAT = '%Y-%m-%d %H.%M.%S'
pre = " 危 "

count = 0
status = 0

def on_info(server, info):
    global bot_list
    if info.is_player == 1:
        if info.content.startswith('!!mr'):
            args = info.content.split(' ')
            if len(args) == 1:
                for line in help_msg.splitlines():
                    server.tell(info.player, line)
            elif args[1] == 'help':
                for line in help_msg.splitlines():
                    server.tell(info.player, line)
            elif args[1] == 'add':
                add_site(server, args, info)
                saveSite()
            elif args[1] == 'list':
                show_site(server)
            elif args[1] == 'reload':
                load_site(site_info)
                server.say("§a监控坐标已重载")
            else:
                server.tell(info.player, "§7[§aMonitor§f/§cWARN§7] §c参数错误，请输入!!mr 查看帮助信息")
    elif info.source == 0 and not info.is_player:
        botinfo = joined_info(info.content)
        if botinfo[0] and botinfo[1] == 'bot' and botinfo[2] not in bot_list:
            bot_list.append(botinfo[2])

def on_load(server, old):
    server.add_help_message('!!mr', '监控插件')
    if not os.path.exists(records):
        os.makedirs(records)
    apart()
    load_site(site_info)

# 分割文件
def apart():
    theTime = datetime.datetime.now().strftime(ISOTIMEFORMAT)
    try:
        shutil.copy(json_filename, './records/' + str(theTime) + '.json')
    except:
        saveJson()

# 保存坐标记录
def saveJson():
    with open(json_filename, 'w+') as f:
        json.dump(record_list, f, ensure_ascii=False, indent=4)

# 保存监控点
def saveSite():
    with open(site_info, 'w') as f:
        json.dump(site_list, f, ensure_ascii=False, indent=4)

# 重载监控点
def load_site(site_info):
    global site_list
    try:
        with open(site_info) as f:
            site_list = json.load(f, encoding='utf8')
    except:
        saveSite()

# 判断整数
def is_instance(str):
    try:
        str = int(str)
        return isinstance(str,int)
    except ValueError:
        return False

# 判断bot
def joined_info(msg):
    joined_player = re.match(
        r'(\w+)\[([0-9\.:]+|local)\] logged in with entity id', msg)
    if joined_player:
        if joined_player.group(2) == 'local':
            return [True, 'bot', joined_player.group(1)]
        else:
            return [True, 'player', joined_player.group(1)]
    return [False]

# 添加监控点
def add_site(server, args, info):
    if len(args) == 7:
        if args[2] in site_list:
            server.tell(info.player, "§7[§aMonitor§f/§cWARN§7] §c监控点已存在")
        elif is_instance(args[3])==0 or is_instance(args[4])==0 or is_instance(args[5])==0:
            server.tell(info.player, "§7[§aMonitor§f/§cWARN§7] §c参数[x] [y] [z]必须为整数")
        elif args[6]=='world' or args[6]=='nether' or args[6]=='end':
            site_list[args[2]] = [args[3], args[4], args[5], args[6]]
            server.say(f"§b{info.player} 添加了新的监控坐标 §e{args[2]}")
        else:
            server.tell(info.player, "§7[§aMonitor§f/§cWARN§7] §c参数[次元]错误")
    else:
        server.tell(info.player, "§7[§aMonitor§f/§cWARN§7] §c缺少参数，请输入!!mr 查看帮助信息")

# 打印监控点
def show_site(server):
    server.say("§b[监控坐标点列表]")
    for key, values in site_list.items():
        x = int(values[0])
        y = int(values[1])
        z = int(values[2])
        dim = values[3]
        server.say(f"§a{key} §b次元: {dim}  §a{x}, {y}, {z}")

# 控制坐标监控开关
def on_player_joined(server, player):
    global count
    global status
    if player in bot_list:
        count = count
    else:
        count = count + 1
        if count == 1:
            status = 1
            monitor(server)
def on_player_left(server, player):
    global count
    global status
    if player in bot_list:
        bot_list.remove(player)
    else:
        count = count - 1
        if count == 0:
            status = 0

# 监控
def monitor(server):
    global record_list
    PI = server.get_plugin_instance('PlayerInfoAPI')
    OP = server.get_plugin_instance('OnlinePlayerAPI')
    while True:
        if status == 1:
            time.sleep(3)
            Online = OP.get_player_list()
            players = list(set(Online) - set(bot_list))
            try:
                for i in range(len(players)):
                    pos = PI.getPlayerInfo(server, players[i], path='Pos')
                    x = int(pos[0])
                    y = int(pos[1])
                    z = int(pos[2])
                    dim = PI.getPlayerInfo(server, players[i], path='Dimension')
                    if dim==0 or dim=="minecraft:overworld":
                        dim = "world"
                    elif dim==-1 or dim=="minecraft:the_nether":
                        dim = "nether"
                    elif dim==1 or dim=="minecraft:the_end":
                        dim = "end"
                    for key, values in site_list.items():
                        fp_x = int(values[0])
                        fp_y = int(values[1])
                        fp_z = int(values[2])
                        fp_dim = values[3]
                        if fp_x-50<=x<=fp_x+50 and fp_z-50<z<fp_z+50 and fp_y-10<=y<=fp_y+10 and dim==fp_dim:
                            server.say("§7[§aMonitor§f/§cWARNING§7]§c" + pre + players[i] + pre + "在 " + key + " 附近游荡！！！")
                    theTime = datetime.datetime.now().strftime(ISOTIMEFORMAT)
                    info = str(theTime) + " " + str(players[i]) + " " + str(dim) + " x:" + str(x)+ " y:" + str(y)+ " z:" + str(z)
                    record_list.append(info)
                    saveJson()
            except:
                continue
            time.sleep(sleep - 3)
        elif status == 0:
            break

def on_unload(server):
    saveJson()
    saveSite()