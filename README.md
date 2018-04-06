# SFTP transfer speed test application

> A simple application that tests the sustained throughput of SFTP connections

## Running the app

The application requires a set of environment variables to be set before
running (see below).

To run the app:

```
python sftp_test.py
```

The application will pull the files from the SFTP server to a local directory
and report the following information:

For each file:

* filename
* file size (in bytes)
* time taken to get the file (as a Python `timedelta`)

On completion it will also report the sum of all file sizes (in MB) and the
sum of time taken to pull all of the files. From this you can calculate the
average throughput (in MB/s).

> **NB** the application **does not** remove the files that it copies (either
from the remote SFTP server or the local directory to which it writes). So if
these files need to be removed after the test, please ensure that this is done
manually.

## Setting the environment variables

If running the application in a remote/temporary session, it is recommended to
create a persistent shell script that will set the environment variables to the
correct values. The `.sh` script should set the following environment variables:

```
export LOG_LEVEL=INFO
export HOST=111.222.333.444:5555 # or known host from /etc/hosts
export USER=user
export PATH_TO_KEY=/absolute/path/to/key
export REMOTE_DIRECTORY_PATH=relative/path/to/source/directory/on/sftp/server
export LOCAL_DIRECTORY_PATH=/absolute/path/to/local/target/directory
export NUM_FILES_TO_SKIP=0
export NUM_FILES_TO_PULL=100
```

You will typically want to vary the `NUM_FILES_TO_SKIP` and `NUM_FILES_TO_PULL`
variables to perform multiple tests.

## Supported authentication methods

This application only supports named user authentication using an SSH key pair.
It does not support password authentication.
