import pytest
from unittest import mock


class TestConnection:
    @pytest.fixture
    def target(self):
        from chaser.connection import Connection as target
        return target

    @mock.patch('chaser.connection.socket.socket')
    def test_make_socket(self, m, target):
        sock = target(None, None).make_socket()
        assert m.called

    @mock.patch('chaser.connection.socket.socket')
    def test_connect(self, m, target):
        conn = target('host', 2009)
        conn.connect()
        assert conn.socket.connect.called
        conn.socket.connect.assert_called_with(('host', 2009))

    @mock.patch('chaser.connection.socket.socket')
    def test_send(self, m, target):
        conn = target('host', 2009)
        conn.connect()
        conn.send(b'abc')
        assert conn.socket.send.called
        conn.socket.send.assert_called_with(b'abc')

    @mock.patch('chaser.connection.socket.socket')
    def test_recv(self, m, target):
        conn = target('host', 2009)
        conn.connect()
        conn.recv()
        assert conn.socket.recv.called
