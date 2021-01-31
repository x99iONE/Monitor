# -*- coding: utf-8 -*-

online_player = []


def on_load(server, old):
    global online_player
    server.register_help_message('!!list', '获取在线玩家列表')
    if old is not None and old.online_player is not None:
        online_player = old.online_player
    else:
        online_player = []


def on_server_stop(server, return_code):
    global online_player
    online_player = []


def on_player_joined(server, player, info):
    if player not in online_player:
        online_player.append(player)


def on_player_left(server, player):
    if player in online_player:
        online_player.remove(player)


def on_info(server, info):
    if info.content == '!!list':
        server.reply(
            info,
            '当前共有{}名玩家在线: {}'.format(len(online_player),
                                     ', '.join(online_player))
        )


def check_online(player: str) -> bool:
    return True if player in online_player else False


def get_player_list() -> list:
    return online_player
