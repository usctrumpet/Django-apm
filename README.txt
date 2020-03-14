Description
This library (MiniAPM) is a small implementation of an Application Performance Monitoring tool.  It is designed to act as middleware for a Django project.  It will report the following information: time the request enters the middleware, time that it leaves the middleware, request path, the parameter list (if any), the MD5 hash value of the rendered output, the current process ID, and the current thread ID.  This information is output to a file which the user can specify.

Django configuration
This file is a middleware file which needs to be specified in the settings.py file for the Django project.  It should be added to the MIDDLEWARE section as <project_name>.miniapm.MiniAPMMiddleware.

Specifying an output file:
The directory structure for the file must exist, but the file itself will be created.
The file that contains the path and name of the output file is out_file_config.py and should be at the root of the project.
See out_file_config.py for the descriptor of specifying the location of the output file

File output
The output of the system will be written to the file specified above.
It will have the following format:
Request Start, Request End, Path, Parameters, MD5, PID, TID
It is possible for a request to not have any parameters; if this is the case, that field will still exist but it will be empty.

This library prints an MD5 hash of the response output.  The MD5 hash is calculated via a function in a shared c library.  The library is called "md5_back.so" and is included in this distribution.  The file can exist anywhere in the file system but its location should be specified in the middleware file "miniapm.py".

The shared c library code is included in a file called md5.c and is compiled for Windows using the following command: gcc -fPIC -shared -o md5_back.so md5.

This library has been tested with Python 2.7 and Python 3.6.

Required files for this library:
<path>/md5_back.so
<path_to_django_project>/miniapm.py
<path_to_django_project>/out_file_config.py

Not required, but can be modified/compiled if desired
md5.c

Not required, but there is a set of tests that can be run as well.
<path_to_project>/tests.py

Not required, just this file :)
README.txt