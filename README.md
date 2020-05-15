# OpenPost

The OpenPost project is intended to allow the creation of an html POST request file, and optionally open the request
in a browser window.  The project provides both a Python module for use within a program, and a stand-alone Python
script that can be used on the command line.

## Python Module

The module provides an ``OpenPost`` class object to prepare and submit html POST requests using the default system internet browser.
It works by writing a temporary html file locally, and then opens the file in the browser.  Upon opening, the file will immediately
submit a form via POST to the target url.

Install using:

``` sh
pip install openpost
```

### OpenPost Object

*class* openpost.**OpenPost**(*url=None, file_name=None, keep_file=False, time_to_live=5, form_data={}, headers=None, body=None, new_tab=True*)

Create a new OpenPost object. All parameters should be passed as keyword arguments. Each parameter is also made available
as a property as described below.

### Properties

- *{str}* OpenPost.**body**  
Additional lines to be added to the \<body\> section of the html document.  If the value is an array, each element will be added on a
separate line.  
*(Added in v0.3)*

- *{str}* OpenPost.**file_name**  
The path and name to use for the output html file.  If no filename is set, it will default to 'OpenPost.html' in the current directory.

- *{dict}* OpenPost.**form_data**  
The `key:value` data to include in the POST request html form.  Each `key` will be entered as a separate item in the form.

- *{str}* OpenPost.**headers**  
Additional lines to be added to the \<head\> section of the html document.  If the value is an array, each element will be added on a
separate line.  
*(Added in v0.3)*

- *{bool}* OpenPost.**keep_file**  
An indicator as to whether or not to keep the output html file after opening in browser.

- *{bool}* OpenPost.**new_tab**  
An indicator as to whether or not to open the page in a new browser tab.  Note that some browsers will force opening in a new tab regardless of this setting.  
*(Added in v0.3)*

- *{float}* OpenPost.**time_to_live**  
The number of seconds to delay before removing the output html file (0-60).  This is ignored if the `keep_file` property is set to `True`.

- *{str}* OpenPost.**url**  
The url for the action field in the html form.

- *{bool}* OpenPost.**written**  
An indicator as to whether or not the html file has already been written.  
*(Depricated since v0.3)*

### Methods

- OpenPost.**clear_data()**  
Clears the data used for the POST request form.

- OpenPost.**add_key(*key*, *value*)**  
Add or update a data key used for the POST request form.  
Arguments:

  - *{str}* key -- Key used in the form
  - *{str}* value -- Value for the specified key

- OpenPost.**delete_key(*key*)**  
Remove a data key used for the POST request form.  
Argument:

  - *{str}* key -- Key to be removed from the form

- OpenPost.**make_html()**  
Make the content of the output html file.  
Returns a string containing the content of the html file, or '' if an error occurred.

- OpenPost.**write_html()**  
Prepare and write the output html file.  
Returns True if the file was successfully written, otherwise False.

- OpenPost.**send_post()**  
Open the output POST html file in the default web browser, automatically writing the output html file if it has not already been written.
Automatically removes the output file after the specified time delay unless the keep_file flag has been set.  
Returns True if the file was successfully opened, otherwise False.

- OpenPost.**version()**  
Returns the version number of the openpost module.

### Example

``` python
import openpost

poster = openpost.OpenPost()
poster.url = 'https://www.somesite.org/login.php'
poster.file_name = 'my_special_filename.html'
poster.add_key('name', 'My Name')
poster.add_key('id', 'My_ID')
poster.add_key('password', 'My_Secret_Password')
poster.body = r'<p>You are being redirected.  Please stand by...</p>'
if poster.send_post():
  print('POST request sent.')
else:
  print('Error sending POST request.')
```

## Command Line Utility

This utility allows you to open a POST request in a browser window from the command line.  It works by writing a
temporary html file locally, and then opens the file in the browser.  Upon opening, the file will immediately submit
a form via POST to the target url.

Please see the [repository on GitHub](https://github.com/rdswift/OpenPost/tree/master/cli) for full usage information and to download.
