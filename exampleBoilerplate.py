#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file is useless without nsmclient.py, which is part of
pynsmclient2 by Nils Hilbricht - 2015
http://www.nilsgey.de
"""

from time import sleep              # main event loop at the bottom of this file
# nsm only
from nsmclient import NSMClient     # will raise an error and exit if this example is not run from NSM.

########################################################################
# General
########################################################################
niceTitle = "myNSMprogram"            # This is the name of your program. This will display in NSM and can be used in your save file

########################################################################
# Prepare the NSM Client
# This has to be done as the first thing because NSM needs to get the paths
# and may quit if NSM environment var was not found.
#
# This is also where to set up your functions that react to messages from NSM,
########################################################################
# Here are some variables you can use:
# ourPath               = Full path to your NSM save file/directory with serialized NSM extension
# ourClientNameUnderNSM = Your NSM save file/directory with serialized NSM extension and no path information
# sessionName           = The name of your session with no path information
########################################################################

def saveCallback(ourPath, sessionName, ourClientNameUnderNSM):
    # Put your code to save your config file in here
    print("saveCallback");


def openCallback(ourPath, sessionName, ourClientNameUnderNSM):
    # Put your code to open your config file in here
    print("openCallback");


def exitProgram(ourPath, sessionName, ourClientNameUnderNSM):
    """This function is a callback for NSM.
    We have a chance to close our clients and open connections here.
    If not nsmclient will just kill us no matter what
    """
    print("exitProgram");
    # Exit is done by NSM kill.


def showGUICallback():
    # Put your code that shows your GUI in here
    print("showGUICallback");
    nsmClient.announceGuiVisibility(isVisible=True)  # Inform NSM that the GUI is now visible. Put this at the end.


def hideGUICallback():
    # Put your code that hides your GUI in here
    print("hideGUICallback");
    nsmClient.announceGuiVisibility(isVisible=False)  # Inform NSM that the GUI is now hidden. Put this at the end.


nsmClient = NSMClient(prettyName = niceTitle,
                      saveCallback = saveCallback,
                      openOrNewCallback = openCallback,
                      showGUICallback = showGUICallback,  # Comment this line out if your program does not have an optional GUI
                      hideGUICallback = hideGUICallback,  # Comment this line out if your program does not have an optional GUI
                      supportsSaveStatus = False,         # Change this to True if your program announces it's save status to NSM
                      exitProgramCallback = exitProgram,
                      loggingLevel = "info", # "info" for development or debugging, "error" for production. default is error.
                      )

# If NSM did not start up properly the program quits here.

########################################################################
# If your project uses JACK, activate your client here
# You can use jackClientName or create your own
########################################################################
jackClientName = nsmClient.ourClientNameUnderNSM

########################################################################
# Start main program loop.
########################################################################

# showGUICallback()  # If you want your GUI to be shown by default, uncomment this line
print("Entering main loop")

while True:
    nsmClient.reactToMessage()  # Make sure this exists somewhere in your main loop
    # nsmClient.announceSaveStatus(False) # Announce your save status (dirty = False / clean = True)
    sleep(0.05)
