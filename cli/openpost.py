#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#################################################################################
#                                                                               #
#   OpenPost - Opens a POST request from the command line in a browser window   #
#   Copyright (C) 2020 Bob Swift                                                #
#                                                                               #
#   Permission is hereby granted, free of charge, to any person obtaining a     #
#   copy of this software and associated documentation files (the "Software"),  #
#   to deal in the Software without restriction, including without limitation   #
#   the rights to use, copy, modify, merge, publish, distribute, sublicense,    #
#   and/or sell copies of the Software, and to permit persons to whom the       #
#   Software is furnished to do so, subject to the following conditions:        #
#                                                                               #
#   The above copyright notice and this permission notice shall be included     #
#   in all copies or substantial portions of the Software.                      #
#                                                                               #
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS     #
#   OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF                  #
#   MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.      #
#   IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY        #
#   CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,        #
#   TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE           #
#   SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.                      #
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
SCRIPT_VERS = '0.05'
SCRIPT_COPYRIGHT = '2019-2020'
SCRIPT_AUTHOR = 'Bob Swift'
SCRIPT_LICENSE = 'GPLv3'

DEFAULT_HTML_FILE = 'openpost.html'
DEFAULT_TIME_TO_LIVE = 5
DEFAULT_STDIN_KEY = 'stdin'

HTML_TEMPLATE = """\
<html>
  <head>
    <title>OpenPost Redirector</title>
  </head>
  <body onLoad="javascript: document.getElementById('postform').submit();">
    <p>Loading...</p>
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
    110: "Invalid POST data item: No key specified.",
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
                            metavar='KEY=VALUE', type=str, nargs='*')
    arg_parser.add_argument("-p", "--file-path", help="Output directory for the temporary HTML file.  Defaults to the current directory.",
                            type=str, metavar='FILEPATH', dest='FILEPATH')
    arg_parser.add_argument("-s", "--stdin", help="Accepts an additional input value from stdin.", action='store_true')
    arg_parser.add_argument("--key", help="Key to use for input from stdin.  Defaults to '{0}'.".format(DEFAULT_STDIN_KEY),
                            type=str, metavar='STDIN_KEY', dest='STDIN_KEY')
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
    if args.post_data:
        form_data = make_form_data_string(args.post_data)
    else:
        form_data = ''

    if 'STDIN_KEY' in vars(args).keys() and getattr(args, 'STDIN_KEY') is not None:
        stdin_key = str(getattr(args, 'STDIN_KEY')).strip()
    else:
        stdin_key = DEFAULT_STDIN_KEY

    from_stdin = ''
    if args.stdin:
        for line in sys.stdin.readlines():
            from_stdin += line
        from_stdin = from_stdin.strip()

    if not form_data and not from_stdin:
        exit_with_error(111)

    if from_stdin:
        form_data += "\n<textarea name='{0}' id='{0}' form='postform' style='display: none;'>{1}</textarea>\n".format(stdin_key, from_stdin.strip())

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
