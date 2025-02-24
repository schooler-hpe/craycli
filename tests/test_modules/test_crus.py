""" Test the crus module.

MIT License

(C) Copyright [2020] Hewlett Packard Enterprise Development LP

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
"""
# pylint: disable=invalid-name
# pylint: disable=too-many-arguments, unused-argument
import json

from ..utils.runner import cli_runner  # pylint: disable=unused-import
from ..utils.rest import rest_mock  # pylint: disable=unused-import


# pylint: disable=redefined-outer-name
def test_cray_crus_usage_info(cli_runner, rest_mock):
    """ Test `cray crus` to make sure the expected commands are available """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['crus'])

    outputs = [
        "cli crus [OPTIONS] COMMAND [ARGS]...",
        "Compute Rolling Upgrade Service",
        "session",
    ]

    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0


# pylint: disable=redefined-outer-name
def test_cray_crus_session_usage_info(cli_runner, rest_mock):
    """ Test `cray crus` to make sure the expected commands are available """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['crus', 'session'])

    outputs = [
        "cli crus session [OPTIONS] COMMAND [ARGS]...",
        "create",
        "delete",
        "describe",
        "list"
    ]
    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0


# pylint: disable=redefined-outer-name
def test_cray_crus_session_create_usage_info(cli_runner, rest_mock):
    """ Test `cray crus` to make sure the expected commands are available """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['crus', 'session', 'create', '--help'])

    outputs = [
        "cli crus session create [OPTIONS]",
        "--upgrade-template-id",
        "--failed-label",
        "--upgrading-label",
        "--starting-label",
        "--upgrade-step-size",
        "--workload-manager-type",
    ]
    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0


# pylint: disable=redefined-outer-name
def test_cray_crus_session_create(cli_runner, rest_mock):
    """Test `cray crus session create` with all options to make sure the
    right data are sent.

    """
    runner, cli, opts = cli_runner
    url_template = '/apis/crus/session'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(
        cli,
        ['crus',
         'session',
         'create',
         '--starting-label',
         'starting-nodes',
         '--failed-label',
         'failed-nodes',
         '--upgrading-label',
         'upgrading-nodes',
         '--workload-manager-type',
         'slurm',
         '--upgrade-step-size',
         '50',
         '--upgrade-template-id',
         'some-string-that-stands-in-for-a-UUID'
        ]
    )
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'post'
    assert data.get('body', None)
    body = data.get('body')
    assert body['starting_label'] == 'starting-nodes'
    assert body['failed_label'] == 'failed-nodes'
    assert body['upgrading_label'] == 'upgrading-nodes'
    assert body['workload_manager_type'] == 'slurm'
    assert body['upgrade_step_size'] == 50
    assert body['upgrade_template_id'] == 'some-string-that-stands-in-for-a-UUID'
    uri = data['url'].split(hostname)[-1]
    assert uri == url_template


# pylint: disable=redefined-outer-name
def test_cray_crus_session_list(cli_runner, rest_mock):
    """Test `cray crus session list` to see that it sends the right
    operation and data.

    """
    # pylint: disable=protected-access
    runner, cli, opts = cli_runner
    url_template = '/apis/crus/session'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(
        cli,
        ['crus', 'session', 'list']
    )
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'get'
    assert data.get('body') is None
    uri = data['url'].split(hostname)[-1]
    assert url_template in uri


# pylint: disable=redefined-outer-name
def test_cray_crus_session_describe(cli_runner, rest_mock):
    """Test `cray crus session describe my-session-id` to see that it
    sends the right operation and data.

    """
    # pylint: disable=protected-access
    runner, cli, opts = cli_runner
    url_template = '/apis/crus/session/my-session-id'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(
        cli,
        ['crus', 'session', 'describe', 'my-session-id']
    )
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'get'
    assert data.get('body') is None
    uri = data['url'].split(hostname)[-1]
    assert url_template in uri


# pylint: disable=redefined-outer-name
def test_cray_crus_session_delete(cli_runner, rest_mock):
    """Test `cray crus session delete my-session-id` to see that it sends
    the right operation and data.

    """
    # pylint: disable=protected-access
    runner, cli, opts = cli_runner
    url_template = '/apis/crus/session/my-session-id'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(
        cli,
        ['crus', 'session', 'delete', 'my-session-id']
    )
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'delete'
    assert data.get('body') is None
    uri = data['url'].split(hostname)[-1]
    assert url_template in uri
