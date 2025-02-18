""" 
FUNCTION FOR GETTING THE ABSOLUTE SERVER PATH
"""
import sys
import os
import platform
import pathlib

#get the os type and store in variable
OS_TYPE = platform.system()

#get the path to the Server project directory
def getServerPath():
    splitter = ""
    #get path to server directory
    #depending on OS_TYPE
    if OS_TYPE == "Windows":
        path_list = os.getcwd().split("\\")
        splitter = "\\"
    elif OS_TYPE == "Linux":
        path_list = str(pathlib.Path().resolve()).split("/")
        splitter = "/"
    else: sys.exit("Error | OS NOT SUPPORTED OR ERROR IN setup.py FILE |")
        
    while path_list[-1] != "Server":
        path_list.pop()
    return splitter.join(path_list)