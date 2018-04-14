#
# 実行方法(Python3.6):
#   python mapper.py ホスト名 ポート番号 チーム名
#
import argparse
from chaser.client import Client
from chaser import const
from chaser.mapping import Map


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

    map = Map()
    x = y = 0  # 自キャラの位置(開始位置基準)
    turn = 0
    while True:
        # @を受信(ターン開始
        control, info = client.receive()
        if control == const.GAME_FINISHED:
            break
        turn += 1
        # gr送信
        control, info = client.get_ready()
        # マップ情報取得
        print(control, info)
        # マップ更新と画面表示
        map.add_surround((x, y), info, turn)
        print(map.as_text((x, y)))
        # コマンド入力
        command = input('command? >')
        # 自キャラの位置を更新
        if command == 'wu':
            y += 1
        elif command == 'wd':
            y -= 1
        elif command == 'wl':
            x -= 1
        elif command == 'wr':
            x += 1
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
