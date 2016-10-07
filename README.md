# pynsm2
Non Session Manager client library in Python - Version2: No dependencies except Python3.

PyNSMClient 2.0 -  A Non Session Manager Client-Library in one file.

Copyright (c) 2014-2016, Nils Hilbricht <nils@hilbricht.net> http://www.hilbricht.com, All rights reserved.

This library is free software; you can redistribute it and/or modify it under the terms of the GNU Lesser General Public

## Short Instructions
Copy nsmclient.py to your program and import and initialize it as early as possible.
Then add nsmClient.reactToMessage to your event loop.

    from nsmclient import NSMClient
    nsmClient = NSMClient(prettyName = niceTitle, #will raise an error and exit if this example is not run from NSM.
        supportsSaveStatus = True,
        saveCallback = saveCallbackFunction,
        openOrNewCallback = openOrNewCallbackFunction,
        exitProgramCallback = exitCallbackFunction,
        loggingLevel = "info", #"info" for development or debugging, "error" for production. default is error.
        )


Don't forget to add nsmClient.reactToMessage to your event loop.

* Each of the callbacks (save, open/new and exit) receive three parameters: ourPath, sessionName, ourClientNameUnderNSM.
* openOrNew gets called first. Init your jack client there with ourClientNameUnderNSM as name.
* exitProgramCallback is the place to gracefully exit your program, including jack-client closing.
* saveCallback gets called all the time. Use ourPath either as filename or as directory.
    * If you choose filename add an extension.
    * If you choose directory make sure that the filenames inside are static, no matter what project/session. The user must have no influence over file naming

The nsmClient object has methods and variables such as:

    nsmClient.ourClientNameUnderNSM  # Always use this name for your program
    nsmClient.announceSaveStatus(False) # Announce your save status (dirty = False / clean = True), If your program sends those messages set supportsSaveStatus = True when intializing NSMClient()
    nsmClient.sessionName

## Long Instructions
* Read and start example.py, then read and understand nsmclient.py. It requires PyQt5 to execute and a brain to read.
* For your own program read and learn the NSM API: http://non.tuxfamily.org/nsm/API.html
* The hard part about session management is not to use this lib or write your own but to make your program comply to the strict rules of session management.

## Sources and Influences
* The Non-Session-Manager by Jonathan Moore Liles <male@tuxfamily.org>: http://non.tuxfamily.org/nsm/
* With help from code fragments from https://github.com/attwad/python-osc ( DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE v2 )
* API documentation: http://non.tuxfamily.org/nsm/API.html

## TODO
* Support for Hiding and Showing the programs GUI
* Convenience for programs that can change the session without restarting.
