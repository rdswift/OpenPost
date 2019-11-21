#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#################################################################################
#                                                                               #
#   OpenPost - Opens a POST request from the command line in a browser window   #
#   Copyright (C) 2019 Bob Swift (rdswift)                                      #
#                                                                               #
#   This program is free software: you can redistribute it and/or modify it     #
#   under the terms of the GNU General Public License as published by the       #
#   Free Software Foundation, either version 3 of the License, or (at your      #
#   option) any later version.                                                  #
#                                                                               #
#   This program is distributed in the hope that it will be useful, but         #
#   WITHOUT ANY WARRANTY; without even the implied warranty of                  #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU           #
#   General Public License for more details.                                    #
#                                                                               #
#   You should have received a copy of the GNU General Public License along     #
#   with this program.  If not, see <https://www.gnu.org/licenses/>.            #
#                                                                               #
#################################################################################
"""
Python script used to open a POST request from the command line in a browser window.
"""

import argparse
import html
import os
import sys
import time
import uuid
import webbrowser

SCRIPT_NAME = 'OpenPost'
SCRIPT_VERS = '0.04'
SCRIPT_COPYRIGHT = '2019'
SCRIPT_AUTHOR = 'Bob Swift'
SCRIPT_LICENSE = 'GPLv3'

DEFAULT_HTML_FILE = 'openpost.html'
DEFAULT_TIME_TO_LIVE = 5

HTML_TEMPLATE = """\
<html>
  <head>
    <title>OpenPost Redirector</title>
  </head>
  <body onLoad="javascript: document.getElementById('postform').submit();">
    <form method="post" name="postform" id="postform" action="{0}">
{1}
    </form>
  </body>
</html>
"""

########################################
#   Error messages and return values   #
########################################

ERRORS = {
    101: "Invalid URL provided: Empty string.",
    102: "Invalid URL provided: Contains spaces.",
    103: "Invalid URL provided: Unspecified error.",
    104: "Invalid temporary file time-to-live.  Must be between 0 and 60 seconds.",
    105: "Invalid temporary file path: Empty string.",
    106: "Invalid temporary file path: Unable to enter.",
    107: "Invalid temporary file name: Empty string.",
    108: "Invalid POST data: Not a list.",
    109: "Invalid POST data item: No key/value separator.",
    110: "Invalid POST data item: No key spacified.",
    111: "Invalid POST data: Empty list.",
}


def random_filename():
    """Provides a unique, random html file name.

    Returns:
        str -- File name
    """
    return uuid.uuid4().hex + '.html'


def date_filename():
    """Provides an html file name based on the current date and time.

    Returns:
        str -- File name
    """
    return time.strftime('%Y%m%d%H%M%S') + '.html'


def exit_with_error(error_number=-1):
    """Print error message and exit with specified error number

    Arguments:
        error_number {int} -- Error number.
    """
    err = int(error_number)
    if err:
        if err in ERRORS:
            print("\n\n{0}\n\n".format(ERRORS[err],))
            sys.exit(err)
        else:
            print("\n\nUnknown error: {0}\n\n".format(err,))
            sys.exit(err)
    else:
        sys.exit(0)


def test_url(url_to_test):
    """Basic testing to check if url is valid.

    Arguments:
        url_to_test {str} -- The url to check

    Returns:
        int -- Error number
    """
    if not isinstance(url_to_test, str):
        return 103
    url = str(url_to_test).strip()
    if not url:
        return 101
    if ' ' in url:
        return 102
    return 0


def parse_command_arguments(args=None):
    """Set up and process command line arguments.

    Returns:
        dict -- Dictionary of arguments and options
    """
    arg_parser = argparse.ArgumentParser(description="{0} (v{1})\nOpens a POST request from the command line in a browser window.".format(SCRIPT_NAME, SCRIPT_VERS,))
    arg_parser.add_argument("url", help="The destination URL to send the POST request.", type=str, metavar='URL')
    arg_parser.add_argument("post_data", help="The POST data to send in the form 'key=value'.  Multiple key/value sets are allowed, separated by spaces.",
                            metavar='KEY=VALUE', type=str, nargs='+')
    arg_parser.add_argument("-p", "--file-path", help="Output directory for the temporary HTML file.  Defaults to the current directory.",
                            type=str, metavar='FILEPATH', dest='FILEPATH')
    group1 = arg_parser.add_mutually_exclusive_group()
    group1.add_argument("-r", "--random-name", help="Set the temporary HTML file name to a random string.", action='store_true')
    group1.add_argument("-d", "--date-name", help="Set the temporary HTML file name to the current date/time string.", action='store_true')
    group1.add_argument("-f", "--file-name", help="Manually set the temporary HTML file name.", type=str, metavar='FILENAME', dest='FILENAME')
    group2 = arg_parser.add_mutually_exclusive_group()
    group2.add_argument("-k", "--keep-file", help="Do not delete the temporary HTML file.", action='store_true')
    group2.add_argument("-t", "--time-to-live", help="Set the number of seconds to wait before deleting the temporary HTML file.", type=float, metavar='SECONDS', dest='SECONDS')
    return arg_parser.parse_args(args)


def make_form_data_string(inputs):
    """Process the POST data input to format form <input> items.

    Arguments:
        inputs {list} -- List of the POST key/value pairs

    Returns:
        str -- POST key/value pairs formatted as form <input> items
    """
    if not isinstance(inputs, list):
        exit_with_error(108)
    data_string = ''
    for item in inputs:
        info = str(item).strip().split('=', 2)
        if len(info) < 2:
            exit_with_error(109)
        key = info[0].strip()
        if key:
            value = html.escape(info[1].strip())
            key = html.escape(key)
            data_string += '{0}<input type="hidden" name="{1}" value="{2}">\n'.format(' ' * 6, key, value,)
        else:
            exit_with_error(110)
    data_string = data_string.strip('\n')
    if not data_string:
        exit_with_error(111)
    return data_string


def make_time_to_live(args):
    """Process the temporary html file time-to-live information.

    Arguments:
        args {object} -- args object from the argparser

    Returns:
        float -- Seconds to delay before deleting the temporary html file
    """
    time_to_live = DEFAULT_TIME_TO_LIVE
    if 'SECONDS' in vars(args) and getattr(args, 'SECONDS') is not None:
        temp = float(getattr(args, 'SECONDS'))
        if 0 < temp <= 60:
            time_to_live = temp
        else:
            exit_with_error(104)
    return time_to_live


def make_file_path(args):
    """Process the temporary html file path information.

    Arguments:
        args {object} -- args object from the argparser

    Returns:
        str -- Path to the directory for storing the temporary html file
    """
    file_path = '.'
    if 'FILEPATH' in vars(args) and getattr(args, 'FILEPATH') is not None:
        temp = str(getattr(args, 'FILEPATH')).strip()
        if not temp:
            exit_with_error(105)
        if not os.path.exists(temp):
            os.makedirs(temp)
        if os.path.isdir(temp):
            file_path = temp
        else:
            exit_with_error(106)
    return file_path


def make_file_name(args):
    """Process the temporary html file name information.

    Arguments:
        args {object} -- args object from the argparser

    Returns:
        str -- The name to use when storing the temporary html file
    """
    html_file = DEFAULT_HTML_FILE
    if args.random_name:
        html_file = random_filename()
    elif args.date_name:
        html_file = date_filename()
    elif 'FILENAME' in vars(args) and getattr(args, 'FILENAME') is not None:
        temp = str(getattr(args, 'FILENAME')).strip()
        if not temp:
            exit_with_error(107)
        if not temp.endswith('.html'):
            temp += '.html'
        html_file = temp
    return html_file


def main():
    """Main processing loop.
    """
    args = parse_command_arguments()

    #######################################
    #   Process the command line inputs   #
    #######################################

    url = str(args.url).strip()
    err = test_url(url)
    if err:
        exit_with_error(err)

    delete_file = True
    if args.keep_file:
        delete_file = False

    time_to_live = make_time_to_live(args)
    file_path = make_file_path(args)
    file_name = make_file_name(args)
    html_file = os.path.join(file_path, file_name)
    form_data = make_form_data_string(args.post_data)

    html_text = HTML_TEMPLATE.format(url, form_data,)

    #################################
    #   Write temporary HTML file   #
    #################################

    with open(html_file, 'w', encoding='utf-8') as output_file:
        output_file.write(html_text)

    webbrowser.open_new_tab(html_file)

    ##################################
    #   Remove temporary HTML file   #
    ##################################

    if delete_file:
        time.sleep(time_to_live)
        if os.path.exists(html_file):
            os.remove(html_file)

##############################################################################


if __name__ == "__main__":
    # execute only if run as a script
    main()
