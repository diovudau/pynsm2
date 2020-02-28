#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyNSMClient 2.1 -  A Non Session Manager Client-Library in one file.

The Non-Session-Manager by Jonathan Moore Liles <male@tuxfamily.org>: http://non.tuxfamily.org/nsm/
With help from code fragments from https://github.com/attwad/python-osc ( DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE v2 )

API documentation: http://non.tuxfamily.org/nsm/API.html

MIT License

Copyright 2014-2020 Nils Hilbricht https://www.laborejo.org

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and 
associated documentation files (the "Software"), to deal in the Software without restriction, 
including without limitation the rights to use, copy, modify, merge, publish, distribute, 
sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is 
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or 
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT 
NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND 
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, 
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT 
OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import base
from time import sleep

def hello(nsmClient):
    nsmClient.broadcast("/index/counter", [hello.i])    
    hello.i += 1
    sleep(1)
hello.i = 0


class BroadcastClient(base.BaseClient):

    def broadcastCallbackFunction(self, ourPath, sessionName, ourClientNameUnderNSM, messagePath, listOfArguments):
        print (f"We are only an example client, but surely it would be valuable to react to {messagePath} for {listOfArguments}")

if __name__ == '__main__':    
    BroadcastClient(eventFunction=hello) #this never returns an object.
