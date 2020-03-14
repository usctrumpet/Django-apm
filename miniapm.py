import sys
import os
import threading
import datetime
import hashlib

from ctypes import *
import ctypes
import out_file_config

class MiniAPMMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        print ("In the init call")

    def __call__(self, request):
        import os

        if sys.version_info[0] < 3:
            import os.path
        else:
            from pathlib import Path

        # Time we enter the middleware
        tinObj = datetime.datetime.now()
        tin = tinObj.strftime("%Y-%m-%dT%H:%M:%S.%f")

        # This is the shared c file that will compute the MD5 hash
        so_file = "c:/code1/myproject/myproject/md5_back.so"
        md5_funct = CDLL(so_file)

        md5_funct.md5_back.restype = ctypes.c_char_p


        # get the file spec
        p = out_file_config.file_path
        n = out_file_config.file_name

        if sys.version_info[0] < 3:
            f_spec = os.path.join(p,n)
            if not os.path.exists(f_spec):
                # we will create it and print the headers as the first entry
                f = open(f_spec, "w+")
                f.write("Request Start, Request End, Path, Parameters, MD5, PID, TID\n")
                f.close()

        else:
            f_spec = Path(p + "/" + n)

            if not f_spec.exists():
                # we will create it and print the headers as the first entry
                f = open(f_spec, "w+")
                f.write("Request Start, Request End, Path, Parameters, MD5, PID, TID\n")
                f.close()
        
        f = open(f_spec, "a+")

        response = self.get_response(request)

        # Get the process ID, thread ID, and path
        pid = str(os.getpid())
        if sys.version_info[0] < 3:
            tid = str(threading.currentThread().ident)
        else:
            tid = str(threading.get_ident())
        path = request.path

        # See if there are any parameters and gather them
        params = dict(request.GET)
        param_string = ''
        for key in params:
            param_string = param_string + key + "; "
        # take off the last 2 characters, they are extra
        params = param_string[:(len(param_string) - 2)]

        # generate MD5 hash
        response_data = response.content
        md5_data = ctypes.create_string_buffer(100)
        md5_data = md5_funct.md5_back(response_data)

        if sys.version_info[0] >= 3:
            md5_data = str(md5_data, 'utf-8')

        # Get the time out of the middleware (a little premature though...)
        toutObj = datetime.datetime.now()
        tout = toutObj.strftime("%Y-%m-%dT%H:%M:%S.%f")

        # Write the results to the date file
        out_string = tin + ", " + tout + ", " + path + ", " + params + ", " + md5_data + ", " + pid + ", " + tid + "\n"
        f.write(out_string)
        f.close()

        # And we're outta here
        return response
