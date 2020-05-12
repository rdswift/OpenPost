# OpenPost

This utility allows you to open a POST request in a browser window from the command line.  It works by writing a temporary HTML file locally, and then opens the file in the browser.  Upon opening, the file will immediately submit a form via POST to the target url.

## Command Line

The utility is called as:

```sh
openpost.py [-h] [-p FILEPATH] [-r | -d | -f FILENAME] [-k | -t SECONDS] URL KEY=VALUE [KEY=VALUE ...]
```

### Required Fields

`URL` is the url to which the POST request is made.

`KEY=VALUE` is the information to include in the form's POST data.  There can be multiple `KEY=VALUE` pairs included on the command line, separated by spaces.

### Options

`-h, --help` displays the help information and exits.

`-p, --file-path FILEPATH` sets the output directory for the temporary HTML file to `FILEPATH`.  If not set, this defaults to the current directory.

`-s, --stdin KEY` sets the form key to use for input read from stdin (pipe or redirect).  If not set, this defaults to 'stdin'.

The file name for the temporary HTML file is set using one of:

- `-r, --random-name` sets the temporary HTML file name to a random string.
- `-d, --date-name` sets the temporary HTML file name to the current date/time string.
- `-f, --file-name FILENAME` sets the temporary HTML file name to the `FILENAME` provided.

These options are mutually exclusive, meaning that one (at most) can be selected per run. If none of these options are selected, the file name for the temporary HTML file will default to `openpost.html`.  Note that if a file exists with the same name as the temporary HTML file being saved, it will be overwritten.

By default, the temporary HTML file will be deleted after 5 seconds.  This should allow sufficient time for the browser to open the file and begin the form submission.  This behavior can be modified by using one of:

- `-k, --keep-file` instructs the program to not delete the temporary HTML file.
- `-t, --time-to-live SECONDS` instructs the program to wait `SECONDS` seconds before deleting the temporary HTML file.  Note that `SECONDS` must be a number greater than 0 and less than or equal to 60.  Both integer and floating point numbers are allowed.

### Error Codes

Some basic checking is performed on the inputs provided on the command line.  If an error is detected, the program will display an error message and exit with an error code.  The errors are:

- `101`: Invalid URL provided: Empty string.
- `102`: Invalid URL provided: Contains spaces.
- `103`: Invalid URL provided: Unspecified error.
- `104`: Invalid temporary file time-to-live.  Must be greater than 0 and less than or equal to 60 seconds.
- `105`: Invalid temporary file path: Empty string.
- `106`: Invalid temporary file path: Unable to enter.
- `107`: Invalid temporary file name: Empty string.
- `108`: Invalid POST data: Not a list.
- `109`: Invalid POST data item: No key/value separator.
- `110`: Invalid POST data item: No key specified.
- `111`: Invalid POST data: Empty list.

If an error occurs during parsing of the command line arguments, the program will exit with an error code of 2.  Examples include:

- No arguments provided.
- Missing `key=value` information.  Note that the first non-option argument is assumed to be the `url`.
- Use of more than one of the mutually exclusive options `-r`, `-d` and `-f`.
- Use of more than one of the mutually exclusive options `-k` and `-t`.

In the event of an Exception error during the process of creating, opening, and deleting the temporary HTML file, the program will halt and the exception information will be displayed.
