from optparse import OptionParser

from nullpochaser.connection import Connection
from nullpochaser.utils import load_class

def main():
    parser = OptionParser()
    parser.add_option('-p', '--port', dest='port', type='int', default=40000)
    parser.add_option('--host', dest='host', default='127.0.0.1')
    parser.add_option('-u', '--username', dest='username', default='hoge')
    parser.add_option('--chaser', dest='chaser', default='nullpochaser.chasers.silent.SilentCHaser')
    options, args = parser.parse_args()

    chaser_class = load_class(options.chaser)
    c = Connection(options.host, options.port)
    ch = chaser_class(c, options.username)
    ch.start()

if __name__ == '__main__':
    main()
