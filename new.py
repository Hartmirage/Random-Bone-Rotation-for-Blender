import bpy
import math
import mathutils
import os
from random import randrange
from random import uniform

#define all needed variables that are set by the user here
NumberOfPoses = 1 #Number of Renders and LabelFiles that will be created
StartAt = 0 #if script was run before and you just want to extend
#Directory = 'D:/blender_projects/handscript/test' #Filepath in witch the output will be saved(windows)
Directory = '/Users/Oliver/Documents/projektarbeit/Handv2mitscript/exports' #(Mac)

#define all needed variables that are set by the script here
#---- needed flags for export labels function
hasWatch = False
hasRing = False
hasSleeve = False

#ActiveCollection = bpy.data.collections["Hand1"] #this is only done to set the right type
HandList = [] #List in which the Hand Collections are Stored

#call this before the mainloop
#---- create Directories and help functions ----
#create Directory to a given path
def createDirectory(path):
    try:
        os.mkdir(path)
    except OSError:
        print('Creation of the directory %s failed' %path)
    else:
        print('Successfully created the directory %s' %path)
        
def createDirectories():
    #create additional directories inside the mainpath for pictures and labels
    ImageFilePath = Directory + '/images' #directory where the image will be saved
    LabelsFilePath = Directory + '/labels' #directory where the labelfiles will be saved
    createDirectory(Directory)
    createDirectory(LabelsFilePath)
    createDirectory(ImageFilePath)



def mainloop():
    print('executed')
    createDirectories()

mainloop()
