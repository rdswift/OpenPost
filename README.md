# OpenPost

This utility allows you to open a POST request in a browser window from the command line.  It works by writing a temporary HTML file locally, and then opens the file in the browser.  Upon opening, the file will immediately submit a form via POST to the target url.

## Command Line

The utility is called as:

```sh
openpost.py [options] url key=value [key=value...]
```

### Required Fields

`url` is the url to which the POST request is made.

`key=value` is the information to include in the form's POST data.  There can be multiple `key=value` pairs included on the command line, separated by spaces.

### Options

`-h, --help` displayed the help information and exits.

`-p, --file-path PATH` sets the output directory for the temporary HTML file to `PATH`.  If not set, this defaults to the current directory.

The file name for the temporary HTML file is set using one of:

- `-r, --random-name` sets the temporary HTML file name to a random string.
- `-d, --date-name` sets the temporary HTML file name to the current date/time string.
- `-f, --file-name NAME` sets the temporary HTML file name to the `NAME` provided.

If none of these options are selected, the file name for the temporary HTML file will default to `openpost.html`.

By default, the temporary HTML file will be deleted after 5 seconds.  This should allow sufficient time for the browser to open the file and begin the form submission.  This behavior can be modified by using one of:

- `-k, --keep-file` instructs the program to not delete the temporary HTML file.
- `-t, --time-to-live SECONDS` instructs the program to wait `SECONDS` seconds before deleting the temporary HTML file.  Note that `SECONDS` must be a number greater than 0 and less than or equal to 60.  Both integer and floating point numbers are allowed.

### Error Codes

Some rudamentary checking is performed on the inputs provided on the command line.  If an error is detected, the program will display an error message and exit with an error code.  The errors are:

- `101`: Invalid URL provided: Empty string.
- `102`: Invalid URL provided: Contains spaces.
- `103`: Invalid URL provided: Unspecified error.
- `104`: Invalid temporary file time-to-live.  Must be between 0 and 60 seconds.
- `105`: Invalid temporary file path: Empty string.
- `106`: Invalid temporary file path: Unable to enter.
- `107`: Invalid temporary file name: Empty string.
- `108`: Invalid POST data: Not a list.
- `109`: Invalid POST data item: No key/value separator.
- `110`: Invalid POST data item: No key spacified.
- `111`: Invalid POST data: Empty list.

In the event of an Exception error during the process of creating, opening, and deleting the temporary HTML file, the program will halt and teh exception information will be displayed.
