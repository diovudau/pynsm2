#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file is useless without nsmclient.py, which is part of
pynsmclient2 by Nils Hilbricht - 2018
http://www.hilbricht.net
"""


print ("This is work in progress. Please use the normal example.py which works with PyQt5")
exit()

import ctypes #xlib and jack
from time import sleep #main event loop at the bottom of this file

#xlib only
from sys import maxsize

#jack only
from random import uniform #to generate samples between -1.0 and 1.0 for Jack.

#nsm only
from nsmclient import NSMClient #will raise an error and exit if this example is not run from NSM.

########################################################################
#General
########################################################################
niceTitle = "PyNSM v2 Example - JACK Noise"

class Values(object):
    def __init__(self):
        self.currentKey = "None"

values = Values()


def titleString():
    s = niceTitle
    return s.encode("ascii")

def savedString():
    """This gets saved in the nsm file
    and can be changed interactively by the user pressing keys"""
    s = "Saved Value: {}".format(values.currentKey)
    return s.encode("ascii")

currentValueString = "None"
def currentString():
    """currentValueString gets changed by the xThread/keypress event"""
    s = "Current Value: {}. Press keys to change.".format(values.currentKey)
    return s.encode("ascii")


########################################################################
#Prepare the NSM Client
#This has to be done as the first thing because NSM needs to get the paths
#and may quit if NSM environment var was not found.
########################################################################

def saveCallback(ourPath, sessionName, ourClientNameUnderNSM):
    global currentValueToBeSaved
    with open(ourPath, "w") as f:  #ourpath is taken as a filename here. We have this path name at our disposal and we know we only want one file. So we don't make a directory. This way we don't have to create a dir first.
        f.write(currentValueToBeSaved)

def openCallback(ourPath, sessionName, ourClientNameUnderNSM):
    global currentValueToBeSaved
    try:
        with open(ourPath, "r") as f:
            currentValueToBeSaved = f.read()
    except FileNotFoundError:
        currentValueToBeSaved = "None. Never Saved."

def exitProgram(ourPath, sessionName, ourClientNameUnderNSM):
    """This function is a callback for NSM.
    We have a chance to close our clients and open connections here.
    If not nsmclient will just kill us no matter what

    We could gracefully close the X11-Client here.
    However, this is another level of complexity: ending threads, etc.
    We just let it crash at the end. No harm done.
    This is only an example after all. Nobody should use pure Xlib for
    a real program. Quitting a program is easily done with a real
    GUI Toolkit like Qt.

    """
    cjack.jack_client_close(ctypesJackClient) #omitting this introduces problems. in Jack1 this would mute all jack clients for several seconds.
    #Exit is done by NSM kill.


nsmClient = NSMClient(prettyName = niceTitle,
                      supportsSaveStatus = True,
                      saveCallback = saveCallback,
                      openOrNewCallback = openCallback,
                      exitProgramCallback = exitProgram,
                      loggingLevel = "info", #"info" for development or debugging, "error" for production. default is error.
                      )

#If NSM did not start up properly the program quits here. No JACK client gets created, no X window can be seen.

########################################################################
#Prepare the JACK Client
#We can't do that without the values we got from nsmClient: path names.
########################################################################
cjack = ctypes.cdll.LoadLibrary("libjack.so.0")
clientName = nsmClient.prettyName
options = 0
status = None
cjack.jack_client_open.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(ctypes.c_int)]  #the two ints are enum and pointer to enum. #http://jackaudio.org/files/docs/html/group__ClientFunctions.html#gab8b16ee616207532d0585d04a0bd1d60

class jack_client_t(ctypes.Structure):
    _fields_ = []

cjack.jack_client_open.restype = ctypes.POINTER(jack_client_t)
ctypesJackClient = cjack.jack_client_open(clientName.encode("ascii"), options, status)

#Create one output port
class jack_port_t(ctypes.Structure):
    _fields_ = []

JACK_DEFAULT_AUDIO_TYPE = "32 bit float mono audio".encode("ascii") #http://jackaudio.org/files/docs/html/types_8h.html
JACK_PORT_IS_OUTPUT = 0x2 #http://jackaudio.org/files/docs/html/types_8h.html
portname = "output".encode("ascii")

cjack.jack_port_register.argtypes = [ctypes.POINTER(jack_client_t), ctypes.c_char_p, ctypes.c_char_p, ctypes.c_ulong, ctypes.c_ulong] #http://jackaudio.org/files/docs/html/group__PortFunctions.html#ga3e21d145c3c82d273a889272f0e405e7
cjack.jack_port_register.restype = ctypes.POINTER(jack_port_t)
outputPort = cjack.jack_port_register(ctypesJackClient, portname,  JACK_DEFAULT_AUDIO_TYPE, JACK_PORT_IS_OUTPUT, 0)

cjack.jack_client_close.argtypes = [ctypes.POINTER(jack_client_t),]

#Create the callback
#http://jackaudio.org/files/docs/html/group__ClientCallbacks.html#gafb5ec9fb4b736606d676c135fb97888b

jack_nframes_t = ctypes.c_uint32
cjack.jack_port_get_buffer.argtypes = [ctypes.POINTER(jack_port_t), jack_nframes_t]
cjack.jack_port_get_buffer.restype = ctypes.POINTER(ctypes.c_float) #this is only valid for audio, not for midi. C Jack has a pointer to void here.

def pythonJackCallback(nframes, void): #types: jack_nframes_t (ctypes.c_uint32), pointer to void
    """http://jackaudio.org/files/docs/html/simple__client_8c.html#a01271cc6cf692278ae35d0062935d7ae"""
    out = cjack.jack_port_get_buffer(outputPort, nframes) #out should be a pointer to jack_default_audio_sample_t (float, ctypes.POINTER(ctypes.c_float))

    #For each required sample
    for i in range(nframes):
        val =  ctypes.c_float(round(uniform(-0.5, 0.5), 10))
        out[i]= val

    return 0 # 0 on success, otherwise a non-zero error code, causing JACK to remove that client from the process() graph.

JACK_CALLBACK_TYPE = ctypes.CFUNCTYPE(ctypes.c_int, jack_nframes_t, ctypes.c_void_p) #the first parameter is the return type, the following are input parameters
callbackFunction = JACK_CALLBACK_TYPE(pythonJackCallback)

cjack.jack_set_process_callback.argtypes = [ctypes.POINTER(jack_client_t), JACK_CALLBACK_TYPE, ctypes.c_void_p]
cjack.jack_set_process_callback.restype = ctypes.c_uint32 #I think this is redundant since ctypes has int as default result type
cjack.jack_set_process_callback(ctypesJackClient, callbackFunction, 0)


#Ready. Activate the client.
cjack.jack_activate(ctypesJackClient)

#The Jack Processing functions gets called by jack in another thread. We just have to keep this program itself running. There is an event loop at the end of this file.


########################################################################
#Prepare the X Window.
########################################################################

cx11 = ctypes.cdll.LoadLibrary("libX11.so")

#from /usr/include/X11/Xlib.h
class Display(ctypes.Structure):
    _fields_ = []

class Screen(ctypes.Structure):
    _fields_ = []

class GC(ctypes.Structure): #Grahic Context http://tronche.com/gui/x/xlib/GC/manipulating.html
    _fields_ = []

#class Window(ctypes.Structure):    _fields_ = []
Window = ctypes.c_ulong  #DAMN IT! Window is not a struct! That was a long bug hunt... keycodes did not show up in the XKeyEvent.

class XKeyEvent(ctypes.Structure):
    """We need all fields in correct order, even though we
    are just interested in the keycode"""
    _fields_ = [
        ("type",ctypes.c_int),
        ("serial", ctypes.c_ulong),
        ("send_event", ctypes.c_int), #bool
        ("display", ctypes.POINTER(Display)),
        ("window", Window),
        ("root", Window),
        ("subwindow", Window),
        ("time", ctypes.c_ulong),  #X.h typedef unsigned long Time;
        ("x", ctypes.c_int),
        ("y", ctypes.c_int),
        ("x_root", ctypes.c_int),
        ("y_root", ctypes.c_int),
        ("state", ctypes.c_uint),
        ("keycode", ctypes.c_uint),
        ("same_screen", ctypes.c_int), #bool
        ]

class XAnyEvent(ctypes.Structure):
    _fields_ = []

class XEvent(ctypes.Union):
  _fields_ = [("type",ctypes.c_int),
              ("xany", XAnyEvent),
              ("xkey", XKeyEvent),
             ] #and others from Xlib.h.


#from /usr/include/X11/Xlib.h
cx11.XOpenDisplay.argtypes = [ctypes.c_char_p]
cx11.XOpenDisplay.restype = ctypes.POINTER(Display)

cx11.XDefaultScreenOfDisplay.argtypes = [ctypes.POINTER(Display)]
cx11.XDefaultScreenOfDisplay.restype = ctypes.POINTER(Screen)

cx11.XRootWindowOfScreen.argtypes = [ctypes.POINTER(Screen)]  #screen number.  even though screen number is an int in Xlib.h we need to treat it as screen here.
cx11.XRootWindowOfScreen.restype = ctypes.POINTER(Window)

cx11.XBlackPixelOfScreen.argtypes = [ctypes.POINTER(Screen)]
cx11.XBlackPixelOfScreen.restype = ctypes.c_ulong

cx11.XWhitePixelOfScreen.argtypes = [ctypes.POINTER(Screen)]
cx11.XWhitePixelOfScreen.restype = ctypes.c_ulong

cx11.XCreateSimpleWindow.argtypes = [ctypes.POINTER(Display), ctypes.POINTER(Window), ctypes.c_int, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_ulong, ctypes.c_ulong] #see below, when the function gets called
cx11.XCreateSimpleWindow.restype = ctypes.POINTER(Window)

cx11.XSelectInput.argtypes = [ctypes.POINTER(Display), ctypes.POINTER(Window), ctypes.c_long,]
cx11.XSelectInput.restype = ctypes.c_int

cx11.XMapWindow.argtypes = [ctypes.POINTER(Display), ctypes.POINTER(Window)]
cx11.XMapWindow.restype = ctypes.c_int

#blocking event grabber
cx11.XNextEvent.argtypes = [ctypes.POINTER(Display), ctypes.POINTER(XEvent)]
cx11.XNextEvent.restype = ctypes.c_int

#non-blocking event grabber. Since we only have one window: no problem.
cx11.XCheckWindowEvent.argtypes = [ctypes.POINTER(Display), ctypes.POINTER(Window), ctypes.c_ulong, ctypes.POINTER(XEvent)]
cx11.XCheckWindowEvent.restype = ctypes.c_int

cx11.XDefaultGCOfScreen.argtypes = [ctypes.POINTER(Screen)]
cx11.XDefaultGCOfScreen.restype = ctypes.POINTER(GC)

cx11.XDrawString.argtypes = [ctypes.POINTER(Display), ctypes.POINTER(Window), ctypes.POINTER(GC), ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_int,]
cx11.XDrawString.restype = ctypes.c_int

cx11.XClearArea.argtypes = [ctypes.POINTER(Display),
                            ctypes.POINTER(Window),
                            ctypes.c_int, #x
                            ctypes.c_int, #y
                            ctypes.c_uint, #width (0 = to the right edge of the window)
                            ctypes.c_uint, #heigth (0 = to the bottom edge of the window)
                            ctypes.c_int, #bool. Send expose event or not. default is not.
                            ]
cx11.XClearArea.restype = ctypes.c_int


#from /usr/include/X11/X.h
EXPOSURE_MASK = int('1000000000000000',2) #digit 15 from right. count from 0  #full: 0000000001000000000000000    #mask for only EXPOSE events
KEYPRESS_AND_EXPOSURE_MASK = int('1000000000000001',2) #digit 1 and 15 from right. count from 0  #full: 0000000001000000000000000  #mask for EXPOSE and KEYPRESS

KEYPRESS = 2
EXPOSE = 12
#Do Stuff
p_display = cx11.XOpenDisplay(None)
p_screen = cx11.XDefaultScreenOfDisplay(p_display)
p_rootWindow = cx11.XRootWindowOfScreen(p_screen)

blackPixel = cx11.XBlackPixelOfScreen(p_screen)
whitePixel = cx11.XWhitePixelOfScreen(p_screen)

p_window = cx11.XCreateSimpleWindow(p_display, #display
                        p_rootWindow,   #parent
                        50,             #x
                        50,             #y
                        370,            #width
                        50,             #height
                        1,              #border_width
                        blackPixel,     #border color
                        whitePixel,     #background color
                        )

cx11.XSelectInput(p_display, p_window, KEYPRESS_AND_EXPOSURE_MASK)  #without the exposure mask XNextEvent in the loop will discard all signals and just block.
cx11.XMapWindow(p_display, p_window)

#Not possible to Ctrl+C. Use the window manager or a posix SIGNAL to quit.
xEvent = XEvent() #mutable.

########################################################################
#Bring it all together. Start main loop and threads.
########################################################################

#Our main Loop to keep the program alive.
#Jack runs our function in its own thread

while True:
    #from /usr/include/X11/X.h
    #The Window is only created after the event loop starts.    #We only receive the following events. Anything else is already prevented by the EXPOSURE_MASK

    #update xEvent in a non-blocking manner.
    cx11.XCheckWindowEvent(p_display, p_window, KEYPRESS_AND_EXPOSURE_MASK, ctypes.byref(xEvent)) #wants &event  in C, which is a reference. ctypes has byref() for that

    #if xEvent.type == EXPOSE:
        #pass

    if xEvent.type == KEYPRESS:
        values.currentKey = xEvent.xkey.keycode
        #nsmClient.announceSaveStatus(False)  #Set save to dirty. Clean is handled by NSM itself.

    cx11.XClearArea(p_display, p_window, 0, 0, 0, 0, 0) #clean everything
    cx11.XDrawString(p_display, p_window, cx11.XDefaultGCOfScreen(p_screen), 15, 30, titleString(), len(titleString()))
    cx11.XDrawString(p_display, p_window, cx11.XDefaultGCOfScreen(p_screen), 15, 45, savedString(), len(savedString()))
    cx11.XDrawString(p_display, p_window, cx11.XDefaultGCOfScreen(p_screen), 15, 60, currentString(), len(currentString()))

    nsmClient.reactToMessage()
    sleep(0.05)
