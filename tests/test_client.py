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

    @mock.patch('chaser.client.Connection')
    def test_send_command(self, m, target):
        c = target('127.0.0.1', 2009, 'cool')
        c.connection = mock.Mock()
        c.send_command(b'wu')
        c.connection.send.assert_called_with(b'wu\r\n')
