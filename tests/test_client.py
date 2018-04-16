import pytest
from unittest import mock


class TestClient:
    @pytest.fixture
    def target(self):
        from chaser.client import Client as target
        return target

    @mock.patch('chaser.client.Connection')
    def test_connect(self, m, target):
        c = target('127.0.0.1', 2009, 'cool')
        c.send_team = mock.Mock()
        c.connect()
        assert c.connection.connect.called

    def test_send_command(self, target):
        c = target('127.0.0.1', 2009, 'cool')
        c.connection = mock.Mock()
        c.send_command(b'wu')
        c.connection.send.assert_called_with(b'wu\r\n')

    def test_receive(self, target):
        c = target('127.0.0.1', 2009, 'cool')
        c.connection = mock.Mock()
        c.connection.recv.return_value = b'1000000000'
        control, info = c.receive()
        assert control == b'1'
        assert info == [0, 0, 0, 0, 0, 0, 0, 0, 0]

    @mock.patch('chaser.client.Client.send_command')
    @mock.patch('chaser.client.Client.receive')
    def test_get_ready(self, m_receive, m_send_command, target):
        c = target('127.0.0.1', 2009, 'cool')
        c.get_ready()
        m_send_command.assert_called_with(b'gr')
