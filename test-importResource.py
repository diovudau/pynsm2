#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyNSMClient 2.0 -  A Non Session Manager Client-Library in one file.
Copyright (c) 2014-2018, Nils Hilbricht <nils@hilbricht.net> http://www.hilbricht.net, All rights reserved.
The Non-Session-Manager by Jonathan Moore Liles <male@tuxfamily.org>: http://non.tuxfamily.org/nsm/
With help from code fragments from https://github.com/attwad/python-osc ( DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE v2 )

API documentation: http//non.tuxfamily.org/nsm/API.html

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 3.0 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library.

Read it here: https://www.gnu.org/licenses/lgpl.html
"""

#Test file for the resource import function in nsmclient.py


if __name__ == "__main__":

    from nsmclient import NSMClient
    #We do not start nsmclient, just the the function with temporary files
    importResource = NSMClient.importResource
    import os, os.path

    import logging
    logging.basicConfig(level=logging.INFO)

    from inspect import currentframe
    def get_linenumber():
        cf = currentframe()
        return cf.f_back.f_lineno

    from tempfile import mkdtemp
    class self(object):
        ourPath = mkdtemp()
        ourClientNameUnderNSM = "Loader Test"
    assert os.path.isdir(self.ourPath)


    #First a meta test to see if our system is working:
    assert os.path.exists("/etc/hostname")
    try:
        result = importResource(self, "/etc/hostname") #should not fail!
    except FileNotFoundError:
        pass
    else:
        print (f"Meta Test System works as of line {get_linenumber()}")
        print ("""You should not see any "Test Error" messages""")
        print ("Working in", self.ourPath)
        print (f"Removing {result} for a clean test environment")
        os.remove(result)
        print()

    #Real tests

    try:
        importResource(self, "/floot/nonexistent") #should fail
    except FileNotFoundError:
        pass
    else:
        print (f"Test Error in line {get_linenumber()}")

    try:
        importResource(self, "////floot//nonexistent/") #should fail
    except FileNotFoundError:
        pass
    else:
        print (f"Test Error in line {get_linenumber()}")

    try:
        importResource(self, "/etc/shadow") #reading not possible
    except PermissionError:
        pass
    else:
        print (f"Test Error in line {get_linenumber()}")


    assert os.path.exists("/etc/hostname")
    try:
        org = self.ourPath
        self.ourPath = "/" #writing not possible
        importResource(self, "/etc/hostname")
    except PermissionError:
        self.ourPath = org
    else:
        print (f"Test Error in line {get_linenumber()}")


    from tempfile import NamedTemporaryFile
    tmpf = NamedTemporaryFile()
    assert os.path.exists("/etc/hostname")
    try:
        org = self.ourPath
        self.ourPath = tmpf.name #writable, but not a dir
        importResource(self, "/etc/hostname")
    except NotADirectoryError:
        self.ourPath = org
    else:
        print (f"Test Error in line {get_linenumber()}")

    #Test the real purpose
    result = importResource(self, "/etc/hostname")
    print ("imported to", result)


    #Test what happens if we try to import already imported resource again
    result = importResource(self, result)
    print ("imported to", result)

    #Test what happens if we try to import a resource that would result in a name collision
    result = importResource(self, "/etc/hostname")
    print ("imported to", result)

    #Count the number of resulting files.
    assert len(os.listdir(self.ourPath)) == 2

