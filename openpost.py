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

import argparse
import html
import os
import time
import urllib
import webbrowser


SCRIPT_NAME = 'OpenPost'
SCRIPT_VERS = '0.01'
SCRIPT_COPYRIGHT = '2019'
SCRIPT_AUTHOR = 'Bob Swift'

HTML_FILE = 'openpost.html'


###############################################
#   Set up command line argument processing   #
###############################################

arg_parser = argparse.ArgumentParser(description="{0} (v{1})\nOpens a POST request from the command line in a browser window.".format(SCRIPT_NAME, SCRIPT_VERS,),
    usage="'openpost.py --help'  or  'openpost.py URL POST_DATA'\n "
)
arg_parser.add_argument("url", help="The destination URL to send the POST request.", metavar='URL')
arg_parser.add_argument("post_data", help="The POST data to send in the form 'key=value'.  Multiple key/value sets are allowed, separated by spaces.",
    metavar='POST_DATA', type=str, nargs='+')

args = arg_parser.parse_args()


#######################################
#   Process the command line inputs   #
#######################################

url = str(args.url).strip()
if not url:
    print('\nInvalid URL (empty): "{0}"\n\n'.format(url,))
    exit(2)

if ' ' in url:
    print('\nInvalid URL (contains spaces): "{0}"\n\n'.format(url,))
    exit(3)

html_text = """
<html>
    <head>
        <title>Open Post Redirector</title>
    </head>
    <body onLoad="javascript: document.getElementById('postform').submit();">
"""
html_text += '        <form method="post" name="postform" id="postform" action="{0}">\n'.format(url,)

for item in args.post_data:
    info = str(item).strip().split('=', 2)
    if len(info) < 2:
        print('\nInvalid POST data item (no key/value separator): "{0}"\n\n'.format(info,))
        exit(4)
    key = info[0].strip()
    if key:
        value = html.escape(info[1].strip())
        key = html.escape(key)
        html_text += '{0}<input type="hidden" name="{1}" value="{2}">\n'.format(' ' * 12, key, value,)
    else:
        print('\nInvalid POST data item (no key spacified): "{0}"\n\n'.format(info,))
        exit(5)

html_text += '        </form>\n    </body>\n</html>\n'

#################################
#   Write temporary HTML file   #
#################################

with open(HTML_FILE, 'w', encoding='utf-8') as f:
    f.write(html_text)

webbrowser.open_new_tab(HTML_FILE)

##################################
#   Remove temporary HTML file   #
##################################

time.sleep(5)
if os.path.exists(HTML_FILE):
    os.remove(HTML_FILE)

# print('URL = {0}\nPOST = {1}\n\n'.format(args.url, args.post_data,))
