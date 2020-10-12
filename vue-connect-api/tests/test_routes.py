from app import routes
import os

import pytest
from pytest_mock import mocker


def test_get_url(monkeypatch):
    assert routes.get_url() == 'http://localhost:8083'

    monkeypatch.setenv('CONNECT_URL', 'http://connect:8083')
    assert routes.get_url() == 'http://connect:8083'
    
def test_new(mocker):
    req = req = mock_request(mocker)
    
    routes.new()
    req.post.assert_called_once_with('http://localhost:8083/connectors/', json={'name': 'foo', 'config': {'bar': '123'}})
    

def test_update(mocker):
    req = mock_request(mocker)

    routes.update('zulu')
    req.put.assert_called_once_with('http://localhost:8083/connectors/zulu/config', json={'name': 'foo', 'bar': '123'})
    

def test_restart(mocker):
    req = mock_request(mocker)
    
    routes.restart('zulu')
    req.post.assert_called_once_with('http://localhost:8083/connectors/zulu/restart')
    
def test_delete(mocker):
    req = mock_request(mocker)

    routes.delete('zulu')
    req.delete.assert_called_once_with('http://localhost:8083/connectors/zulu')

def test_pause(mocker):
    req = mock_request(mocker)

    routes.pause('zulu')
    req.put.assert_called_once_with('http://localhost:8083/connectors/zulu/pause')

def test_resume(mocker):
    req = mock_request(mocker)

    routes.resume('zulu')
    req.put.assert_called_once_with('http://localhost:8083/connectors/zulu/resume')

def test_task_restart(mocker):
    req = mock_request(mocker)

    routes.task_restart('zulu', '0')
    req.post.assert_called_once_with('http://localhost:8083/connectors/zulu/tasks/0/restart')

def test_config(mocker):
    req = mock_request(mocker)

    routes.config('zulu')
    req.get.assert_called_once_with('http://localhost:8083/connectors/zulu/config')

def test_connectors(mocker):
    mocker.patch('app.routes.request')

    class Resp:
        def __init__(self, url):
            self.url = url

        def json(self):
            if 'status' in self.url:
                return {'name': 'foo'}
            else:
                return ['foo', 'bar']

    class Req:
        called = []
        def get(self, url):
            self.called.append(url)
            return Resp(url)

    mock = Req()
    mocker.patch('app.routes.requests', mock)
    
    mocker.patch('app.routes.jsonify', jsonify)

    routes.connectors()

    assert len(mock.called) == 3
    assert 'http://localhost:8083/connectors/foo/status' in mock.called
    assert 'http://localhost:8083/connectors/bar/status' in mock.called
    assert 'http://localhost:8083/connectors' in mock.called

def test_status(mocker):
    req = mock_request(mocker)

    routes.status('zulu')
    req.get.assert_called_once_with('http://localhost:8083/connectors/zulu/status')

def test_validate(mocker):
    req = mock_request(mocker)

    routes.validate('zulu')
    req.put.assert_called_once_with('http://localhost:8083/connector-plugins/zulu/config/validate', json={'name': 'foo', 'bar': '123'})


def test_plugins(mocker):
    req = mock_request(mocker)

    routes.plugins()
    req.get.assert_called_once_with('http://localhost:8083/connector-plugins')

def test_info(mocker):
    req = mock_request(mocker)

    routes.info()
    req.get.assert_called_once_with('http://localhost:8083')

def mock_request(mocker):
    data = mocker.patch('app.routes.request')
    data.get_json = lambda: {'name': 'foo', 'bar': '123'}

    req = mocker.patch('app.routes.requests')

    mocker.patch('app.routes.jsonify', jsonify)

    return req

def jsonify(x):
    return x
