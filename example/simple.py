#
# 実行方法(Python3.6):
#   python simple.py ポート番号 チーム名
#
import sys
from chaser.client import Client
from chaser import const

host = '127.0.0.1'  # 接続先ホスト名
port = int(sys.argv[1])  # ポート番号
username = sys.argv[2]  # チーム名
client = Client(host, port, username)
# 接続
client.connect()
# チーム名を送信
client.username()

while True:
    # @を受信(ターン開始
    control, info = client.receive()
    if control == const.GAME_FINISHED:
        break
    # gr送信
    control, info = client.get_ready()
    # マップ情報取得
    print(control, info)
    # コマンド入力
    print('command? >', end='')
    command = input()
    # コマンド送信
    client.send_command(command.encode('ascii'))
    # マップ情報取得
    control, info = client.receive()
    if control == const.GAME_FINISHED:
        break
    # ターン終了
    client.turn_end()
