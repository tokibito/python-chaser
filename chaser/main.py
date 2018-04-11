from optparse import OptionParser

from nullpochaser.connection import Connection
from nullpochaser.utils import load_class


def start(host='127.0.0.1', port=40000, username='hoge',
          klass='nullpochaser.chasers.silent.SilentCHaser'):
    """クライアントを開始する関数
    """
    chaser_class = load_class(klass)
    c = Connection(host, port)
    ch = chaser_class(c, username)
    ch.start()


def main():
    parser = OptionParser()
    parser.add_option('-p', '--port', dest='port', type='int', default=40000)
    parser.add_option('--host', dest='host', default='127.0.0.1')
    parser.add_option('-u', '--username', dest='username', default='hoge')
    parser.add_option(
        '--chaser', dest='chaser',
        default='nullpochaser.chasers.silent.SilentCHaser')
    options, args = parser.parse_args()
    start(options.host, options.port, options.username, options.chaser)


if __name__ == '__main__':
    main()
