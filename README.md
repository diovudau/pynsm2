# pynsm2
Non Session Manager client library in Python - Version2: No dependencies except Python3.

PyNSMClient 2.0 -  A Non Session Manager Client-Library in one file.

Copyright (c) 2015, Nils Gey <ich@nilsgey.de> http://www.nilsgey.de, All rights reserved.

This library is free software; you can redistribute it and/or modify it under the terms of the GNU Lesser General Public

Short Instructions:
Copy nsmclient.py to your program and import and initialize it as early as possible

    from nsmclient import NSMClient
    nsmClient = NSMClient(prettyName = niceTitle, #will raise an error and exit if this example is not run from NSM.
        supportsSaveStatus = True,
        saveCallback = saveCallbackFunction,
        openOrNewCallback = openOrNewCallbackFunction,
        exitProgramCallback = exitCallbackFunction,
        loggingLevel = "info", #"info" for development or debugging, "error" for production. default is error.
        )

* Each of the callbacks (save, open/new and exit) receive three parameters: ourPath, sessionName, ourClientNameUnderNSM.
* openOrNew gets called first. Init your jack client there with ourClientNameUnderNSM as name.
* exitProgramCallback is the place to gracefully exit your program, including jack-client closing.
* saveCallback gets called all the time. Use ourPath either as filename or as directory. If you choose a directory make sure that the filenames inside are static, no matter what session, and that the user has no influence over them.

There are some functions in nsmClient you can call directly, without a callback. Such as announcing your save status (dirty/clean):

    nsmClient.announceSaveStatus(False)

If your program sends those messages set supportsSaveStatus = True when intializing NSMCLient()

Long Instructions:
Read and start example.py, then read and understand nsmclient.py. It requires PyQt5 to execute and a brain to read.
For your own program read and learn the NSM API: http://non.tuxfamily.org/nsm/API.html
The hard part about session management is not to use this lib or write your own but to make your program comply to the strict rules of session management.


Sources and Influences:
The Non-Session-Manager by Jonathan Moore Liles <male@tuxfamily.org>: http://non.tuxfamily.org/nsm/
With help from code fragments from https://github.com/attwad/python-osc ( DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE v2 )
API documentation: http://non.tuxfamily.org/nsm/API.html

TODO:
* Support for Hiding and Showing the programs GUI
* Convenience for programs that can change the session without restarting.
