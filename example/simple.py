#
# 実行方法(Python3.6):
#   python simple.py ホスト名 ポート番号 チーム名
#
import argparse
from chaser.client import Client
from chaser import const


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='127.0.0.1', help='接続先ホスト名')
    parser.add_argument('--port', type=int, default=2009, help='接続先ポート番号')
    parser.add_argument('--team', default='Cool', help='チーム名')
    args = parser.parse_args()

    print("接続先ホスト:", args.host)
    print("接続先ポート:", args.port)
    print("チーム名:", args.team)
    client = Client(args.host, args.port, args.team)
    # 接続
    client.connect()
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
        command = input('command? >')
        # コマンド送信
        client.send_command(command.encode('ascii'))
        # マップ情報取得
        control, info = client.receive()
        if control == const.GAME_FINISHED:
            break
        # ターン終了
        client.turn_end()


if __name__ == '__main__':
    main()
