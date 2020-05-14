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

*class* openpost.**OpenPost**(*url=None, file_name=None, keep_file=False, time_to_live=5, form_data={}*)

Create a new OpenPost object. All parameters should be passed as keyword arguments. Each parameter is also made available
as a property as described below.

### Properties

- *{str}* OpenPost.**file_name**  
The path and name to use for the output html file.

- *{dict}* OpenPost.**form_data**  
The `key:value` data to include in the POST request html form.  Each `key` will be entered as a separate item in the form.

- *{bool}* OpenPost.**keep_file**  
An indicator as to whether or not to keep the output html file after opening in browser.

- *{float}* OpenPost.**time_to_live**  
The number of seconds to delay before removing the output html file (0-60).  This is ignored if the `keep_file` property is set to `True`.

- *{str}* OpenPost.**url**  
The url for the action field in the html form.

- *{bool}* OpenPost.**written**  
An indicator as to whether or not the html file has already been written.

### Methods

- OpenPost.**clear_data()**  
Clears the data used for the POST request form.

- OpenPost.**add_key(*key*, *value*)**  
Add or update a data key used for the POST request form.  
Arguments:

  - key {str} -- Key used in the form
  - value {str} -- Value for the specified key

- OpenPost.**delete_key(*key*)**  
Remove a data key used for the POST request form.  
Argument:

  - key {str} -- Key to be removed from the form

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

## Command Line Utility

This utility allows you to open a POST request in a browser window from the command line.  It works by writing a
temporary html file locally, and then opens the file in the browser.  Upon opening, the file will immediately submit
a form via POST to the target url.

Please see the [repository on GitHub](https://github.com/rdswift/OpenPost/tree/master/cli) for full usage information and to download.
