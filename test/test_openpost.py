#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for the OpenPost project
"""

import pytest
import time
import openpost as test_module


class ArgsObject(object):
    """
    Temporary object used for testing to mimic the args object
    returned by argparse.
    """
    date_name = False
    random_name = False
    FILENAME = None
    FILEPATH = None
    keep_file = False
    SECONDS = None
    url = None
    post_data = None


def test_date_name():
    name = test_module.date_filename()
    assert len(name) == 19
    assert name.startswith(time.strftime('%Y%m%d'))
    assert name.endswith('.html')


def test_uuid_name():
    name = test_module.random_filename()
    assert len(name) == 37
    assert name.endswith('.html')


def test_make_file_name_01():
    args = ArgsObject()
    args.date_name = True
    args.random_name = False
    args.FILENAME = 'Test File Name'
    name = test_module.make_file_name(args)
    assert len(name) == 19
    assert name.startswith(time.strftime('%Y%m%d'))
    assert name.endswith('.html')


def test_make_file_name_02():
    args = ArgsObject()
    args.date_name = False
    args.random_name = True
    args.FILENAME = 'Test File Name'
    name = test_module.make_file_name(args)
    assert len(name) == 37
    assert name.endswith('.html')


def test_make_file_name_03():
    args = ArgsObject()
    args.date_name = False
    args.random_name = False
    args.FILENAME = 'Test File Name'
    name = test_module.make_file_name(args)
    assert len(name) == 19
    assert name.endswith('.html')
    assert name.startswith('Test File Name')


def test_make_file_name_04():
    args = ArgsObject()
    args.date_name = False
    args.random_name = False
    name = test_module.make_file_name(args)
    assert name == test_module.DEFAULT_HTML_FILE
    assert name.endswith('.html')


def test_make_file_path_01():
    args = ArgsObject()
    args.date_name = False
    args.random_name = False
    name = test_module.make_file_path(args)
    assert name == '.'


def test_make_file_path_02():
    args = ArgsObject()
    args.FILEPATH = 'test_FILE_path'
    args.random_name = False
    name = test_module.make_file_path(args)
    assert name == 'test_FILE_path'


def test_single_post_data():
    data = test_module.make_form_data_string(['abc=123'])
    assert '<input type="hidden" name="abc" value="123">' in data


def test_multiple_post_data():
    data = test_module.make_form_data_string(['abc=123', 'xyz=456'])
    assert '<input type="hidden" name="abc" value="123">' in data
    assert '<input type="hidden" name="xyz" value="456">' in data


def test_post_data_case():
    data = test_module.make_form_data_string(['abc=123'])
    assert '<input type="hidden" name="ABC" value="123">' not in data


def test_test_url_01():
    data = test_module.test_url(1)
    assert data == 103


def test_test_url_02():
    data = test_module.test_url('')
    assert data == 101


def test_test_url_03():
    data = test_module.test_url(' ')
    assert data == 101


def test_test_url_04():
    data = test_module.test_url('embedded space')
    assert data == 102


def test_test_url_05():
    data = test_module.test_url('localhost')
    assert data == 0


def test_test_url_06():
    data = test_module.test_url('192.168.1.1')
    assert data == 0


def test_test_url_07():
    data = test_module.test_url('www.somewhere.com')
    assert data == 0


def test_test_url_08():
    data = test_module.test_url('http://www.somewhere.com')
    assert data == 0


def test_test_url_09():
    data = test_module.test_url('https://www.somewhere.com')
    assert data == 0


def test_test_url_10():
    data = test_module.test_url('www.somewhere.com/')
    assert data == 0


def test_test_url_11():
    data = test_module.test_url('www.somewhere.com/subdir')
    assert data == 0


def test_test_url_12():
    data = test_module.test_url('www.somewhere.com/subdir/')
    assert data == 0


def test_test_ttl_01():
    args = ArgsObject()
    args.SECONDS = None
    data = test_module.make_time_to_live(args)
    assert data == test_module.DEFAULT_TIME_TO_LIVE


def test_test_ttl_02():
    args = ArgsObject()
    args.SECONDS = 10
    data = test_module.make_time_to_live(args)
    assert data == 10


def test_test_ttl_03():
    args = ArgsObject()
    args.SECONDS = 13.5
    data = test_module.make_time_to_live(args)
    assert data == 13.5


def test_exit_missing(capsys):
    args = ArgsObject()
    args.url = ''
    with pytest.raises(SystemExit) as err:
        test_module.exit_with_error()
    assert err.value.code == -1


def test_exit_unknown(capsys):
    args = ArgsObject()
    args.url = ''
    with pytest.raises(SystemExit) as err:
        test_module.exit_with_error(-1)
    assert err.value.code == -1


def test_exit_101(capsys):
    args = ArgsObject()
    args.url = ''
    with pytest.raises(SystemExit) as err:
        test_module.exit_with_error(101)
    assert err.value.code == 101


def test_make_ttl_e104_1(capsys):
    args = ArgsObject()
    args.SECONDS = -1
    with pytest.raises(SystemExit) as err:
        test_module.make_time_to_live(args)
    assert err.value.code == 104


def test_make_ttl_e104_2(capsys):
    args = ArgsObject()
    args.SECONDS = 61
    with pytest.raises(SystemExit) as err:
        test_module.make_time_to_live(args)
    assert err.value.code == 104


def test_make_path_e105_1(capsys):
    args = ArgsObject()
    args.FILEPATH = ''
    with pytest.raises(SystemExit) as err:
        test_module.make_file_path(args)
    assert err.value.code == 105


def test_make_path_e105_2(capsys):
    args = ArgsObject()
    args.FILEPATH = ' '
    with pytest.raises(SystemExit) as err:
        test_module.make_file_path(args)
    assert err.value.code == 105


def test_make_path_e106(capsys):
    args = ArgsObject()
    args.FILEPATH = 'openpost.py'
    with pytest.raises(SystemExit) as err:
        test_module.make_file_path(args)
    assert err.value.code == 106


def test_make_name_e107_1(capsys):
    args = ArgsObject()
    args.FILENAME = ''
    with pytest.raises(SystemExit) as err:
        test_module.make_file_name(args)
    assert err.value.code == 107


def test_make_name_e107_2(capsys):
    args = ArgsObject()
    args.FILENAME = ' '
    with pytest.raises(SystemExit) as err:
        test_module.make_file_name(args)
    assert err.value.code == 107


def test_make_data_e108_1(capsys):
    with pytest.raises(SystemExit) as err:
        test_module.make_form_data_string('')
    assert err.value.code == 108


def test_make_data_e108_2(capsys):
    with pytest.raises(SystemExit) as err:
        test_module.make_form_data_string(0)
    assert err.value.code == 108


def test_make_data_e108_3(capsys):
    with pytest.raises(SystemExit) as err:
        test_module.make_form_data_string(1.5)
    assert err.value.code == 108


def test_make_data_e108_4(capsys):
    with pytest.raises(SystemExit) as err:
        test_module.make_form_data_string(('a', 'b'))
    assert err.value.code == 108


def test_make_data_e108_5(capsys):
    with pytest.raises(SystemExit) as err:
        test_module.make_form_data_string({'key': 'value'})
    assert err.value.code == 108


def test_make_data_e109(capsys):
    with pytest.raises(SystemExit) as err:
        test_module.make_form_data_string(['no equals sign'])
    assert err.value.code == 109


def test_make_data_e110(capsys):
    with pytest.raises(SystemExit) as err:
        test_module.make_form_data_string(['=no key'])
    assert err.value.code == 110


def test_make_data_e111(capsys):
    with pytest.raises(SystemExit) as err:
        test_module.make_form_data_string([])
    assert err.value.code == 111


def test_main_e0_1(capsys):
    with pytest.raises(SystemExit) as err:
        test_module.parse_command_arguments(['--help'])
    assert err.value.code == 0


def test_main_e0_2(capsys):
    with pytest.raises(SystemExit) as err:
        test_module.parse_command_arguments(['-h'])
    assert err.value.code == 0


def test_main_e2_1(capsys):
    with pytest.raises(SystemExit) as err:
        test_module.parse_command_arguments([])
    assert err.value.code == 2


def test_main_e2_2(capsys):
    with pytest.raises(SystemExit) as err:
        test_module.parse_command_arguments(['localhost'])
    assert err.value.code == 2


def test_main_e2_3(capsys):
    with pytest.raises(SystemExit) as err:
        test_module.parse_command_arguments(['localhost', 'key=value', '-r', '-d'])
    assert err.value.code == 2


def test_main_e2_4(capsys):
    with pytest.raises(SystemExit) as err:
        test_module.parse_command_arguments(['localhost', 'key=value', '-r', '-f', 'filename'])
    assert err.value.code == 2


def test_main_e2_5(capsys):
    with pytest.raises(SystemExit) as err:
        test_module.parse_command_arguments(['localhost', 'key=value', '-d', '-f', 'filename'])
    assert err.value.code == 2


def test_main_e2_6(capsys):
    with pytest.raises(SystemExit) as err:
        test_module.parse_command_arguments(['localhost', 'key=value', '-k', '-t', '5'])
    assert err.value.code == 2
