import bpy
import math
import mathutils
import os
from random import randrange
from random import randint
from random import uniform

#define all needed variables that are set by the user here -----------------------------------------------------------------------------------
NumberOfPoses = 1 #Number of wanted results 
StartAt = 0 #if script was run before and an enhancement of the dataset is wanted, set the index accordingly.
#if the dataset features the files 0 to 100 set the StartAt variable to 101.
Directory = 'D:/blender_projects/handscript/test' #Filepath in witch the output will be saved(windows)-------------------------WINDOWS FORMAT
#Directory = '/Users/Oliver/Documents/projektarbeit/Handv2mitscript/exports' #-----------------------------------------------------MAC FORMAT

#define all needed variables that are set by the script here----------------------------------------------------------------------------------
#booleans will be set via the script and will later be exported in the labels file
hasWatch = False
hasRing = False
hasSleeve = False

ActiveCollection = bpy.data.collections["CollectionHand1"] #set ActiveCollection to Hand 1 at start
HandList = []

#call this before the mainloop
#---------------------create Directories and everything that is used by the function ---------------------------------------------------------

#creates the Directory with a given path --- helpmethod for createDirectories
def createDirectory(path):
    try:
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)

#this makes sure the main Directory exists, as well as the Directories for the renders and the labels
def createDirectories():
    #create additional directories inside the mainpath for pictures and labels
    ImageFilePath = Directory + '/images' #directory where the images will be saved
    LabelsFilePath = Directory + '/labels' #directory where the labelfiles will b saved
    #take the defined filepaths for export and make sure they exist(create them)
    createDirectory(Directory)
    createDirectory(LabelsFilePath)
    createDirectory(ImageFilePath)
    
#object to Hold information of Hand
class Hand:
  def __init__(self, collection, watches, rings, clothes, rig):
    self.collection = collection
    self.watches = watches
    self.rings = rings
    self.clothes = clothes
    self.rig = rig

def getSubString(string, startIndex, endIndex):
    returnString = ''
    for i in range(startIndex, endIndex):
        returnString += string[i]
    return returnString

def getSubCollection(string):
    List = []
    for col in bpy.data.collections:
        if string in col.name:
            List.append(col)
    return List  

def getRig(string):
    for rig in bpy.data.objects:
        if string in rig.name:
            return rig

def initHands():
    for x in bpy.data.collections:
        if "CollectionHand" in x.name:
            #HandList.append(Hand())
            Name = getSubString(x.name, len(x.name)-5, len(x.name))
            Collection = x
            Watch = getSubCollection(Name + "Watch")
            HandList.append(Hand(x,
                                    getSubCollection(Name + "Watch"),
                                    getSubCollection(Name + "Ring"),
                                    getSubCollection(Name + "Cloth"),
                                    getRig(Name + "Rig")))

def hideAllHands():
    #before the mainloop hide all hand collections
    for x in HandList:
        x.collection.hide_viewport = True      

#this method need to run before the main loop to prepare all the collections and directories
def init():    
    createDirectories()
    initHands()
    hideAllHands()


#call this inside the mainloop
def unhideOne(Hand):
    Hand.collection.hide_viewport = False  
    
def hideHand(Hand):
    Hand.collection.hide_viewport = True

def randomize(Hand):
    #hide all watches, rings and sleeves
    for x in Hand.watches:
        x.hide_viewport = True
    for x in Hand.rings:
        x.hide_viewport = True
    for x in Hand.clothes:
        x.hide_viewport = True
    
    numOfWatches = len(Hand.watches)
    randWatch = 0    
    if numOfWatches != 0:
        randWatch = randint(0, numOfWatches) 
    if randWatch != 0 and numOfWatches != 0:
        Hand.watches[randWatch - 1].hide_viewport = False
        hasWatch = True
    else:
        hasWatch = False
    
    numOfRings = len(Hand.rings)
    randRing = 0
    if numOfRings != 0:
        randRing = randint(0, numOfRings)
    if randRing != 0 and numOfRings != 0:
        Hand.rings[randRing - 1].hide_viewport = False
        hasRing = True
    else:
        hasRing = False
        
    numOfClothes = len(Hand.clothes)
    randCloth = 0
    if numOfClothes != 0:
        randCloth = randint(0, numOfClothes)
    if randCloth != 0 and numOfClothes != 0:
        Hand.clothes[randCloth - 1].hide_viewport = False
        hasSleeve = True
    else:
        hasSleeve = False
    



def prepareHand(index):
    #choose one hand, set as active, unhide the collection of active hand
    #hide/unhide clothes, ring and watch (randomized)
    #rotate bones randomized within the limits of the constraints
    pass
    
#####insert all methods helping the prepare method underneath

#def export():
    #export labels: right/left, hasWatch(bool), hasRing(bool), hasSleeve(bool)
    #export labels for each bone(position, rotation??)
    #render image and save
    #render tiefenbild?
    
#####insert all methods helping the export method underneath

#def reset():
    #reset rotation of bones
    #hide the active hand collection

def loop():
    #choose one Hand random
    temp = len(HandList)
    HandIndex = randrange(temp)
    Hand = HandList[HandIndex]
    #unhide it
    unhideOne(Hand)
    
    #randomizeClothing and Rotate Bones
    randomize(Hand)
    
    resetBones(Hand.rig)
    rotateBones(Hand.rig)
    
    
    
    
    
    
    #hide it again
    #hideHand(HandIndex) ##-----------------------------------------------------------uncomment when run in loop



#------------------------------------------------------------------------------------------------------------ main loop

#rotates a single bone within the limits of the constaint
def rotateBone(self):
    self.rotation_mode = 'XYZ'
    self.rotation_euler.rotate_axis('X', uniform(self.constraints[0].min_x, self.constraints[0].max_x))
    self.rotation_euler.rotate_axis('Y', uniform(self.constraints[0].min_y, self.constraints[0].max_y))
    self.rotation_euler.rotate_axis('Z', uniform(self.constraints[0].min_z, self.constraints[0].max_z))
    #print(self)

#does the single bone rotation for all bones that have a constraint
def rotateBones(Rig):
    for x in (Rig.pose.bones):
        try:
            rotateBone(x)
        except:
            pass

#resets a single bone to the neutral pose
def resetBone(self):
    self.rotation_mode = 'AXIS_ANGLE'
    self.rotation_axis_angle[0] = 0.0
    self.rotation_axis_angle[1] = 0.0
    self.rotation_axis_angle[2] = 0.0
    self.rotation_axis_angle[3] = 0.0

#does the single bone reset for all bones
def resetBones(Rig):
    for x in (Rig.pose.bones):
        try:
            resetBone(x)
        except:
            pass
        
#rotates all bones, renders the image and resets the bones
def rotateAndRender(counter, Rig):
    rotateBones(Rig)
    renderImage(counter)
    exportLabels(counter, Rig)
    resetBones(Rig)

#renders image and saves it at the given path at the top of the script
def renderImage(counter):
    bpy.context.scene.camera = bpy.data.objects["Camera"]
    path = ImageFilePath + '/' + str(counter) + '.png'
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    bpy.context.scene.render.filepath = path
    bpy.ops.render.render(write_still = 1)

#formats the float to supress 1*e10 etc. format
def formatFloat(float):
    return '{:.12f}'.format(float)

#writes name of bone, HeadLocationVector and TailLocationVector in txt file for each bone
def exportLabels(counter, Rig):
    path = LabelsFilePath + '/' + str(counter) + '.txt'
    f = open(str(path), 'w')
    for x in (Rig.pose.bones):
        try:
            headX = formatFloat(x.head[0])
            HeadY = formatFloat(x.head[1])
            HeadZ = formatFloat(x.head[2])
            TailX = formatFloat(x.tail[0])
            TailY = formatFloat(x.tail[1])
            TailZ = formatFloat(x.tail[2])
            
            
            f.write(x.name + ': HeadLocation: (' + str(headX) + ', ' + str(HeadY) + ', ' + str(HeadZ) + ')')
            f.write(' TailLocation: (' + str(TailX) + ', ' + str(TailY) + ', ' + str(TailZ) + ')')
            f.write('\n')
        except:
            pass
    f.close()



def main():
    #select ActiveRig
    ActiveRig = getActiveRig()
    
    #set ARig to active Object to make sure that enabling Pose Mode is possible
    bpy.context.view_layer.objects.active = ActiveRig
    #make sure to be in POSE mode, so the rotation will show in the rendered Image(in Object mode you won't see the difference)
    bpy.ops.object.mode_set(mode='POSE')
    
    #setting the Path Variables
    #needs to be global to get the FilePath Varibale from the top. leaving out "global" would create a new local Variable
    global FilePath
    FilePath = Directory + '/' + ActiveRig.name
    global ImageFilePath
    ImageFilePath = FilePath + '/images' #directory where the images will be saved
    global LabelsFilePath
    LabelsFilePath = FilePath + '/labels' #directory where the labelfiles will b saved
    
    #creates needed Directorys
    createDirectory(FilePath)
    createDirectory(LabelsFilePath)
    createDirectory(ImageFilePath)
    
    #loop for the wanted number of images
    for i in range(StartAt, StartAt + NumberOfPoses):
        rotateAndRender(i, ActiveRig)
        print(i)
        
def hideExcept(Hand):
    for x in HandList:
        x.collection.hide_viewport = True
    try:       
        Hand.collection.hide_viewport = False
    except:
        print('Index out of Bounds')
        
def testing():
    initHands()
    L = bpy.context.view_layer
    hideExcept(HandList[1])
    
    
init()
loop()

 
#kleidungsstücke zufällig und im export file labeln
#links rechts labeln
#tiefenbild(opencv)

#letztlicher ablauf in pseudo:
#Pfade setzen und ordner generiern
#Hände(class) erstellen und in Liste adden
#zufällig alle ausser einer Hand ausblenden
#zufällig Kleidung, Ring und Uhr ein/ausblenden
#Bones zufällig rotieren
#Position der Bones, sowie Kleidung(bool) Uhr(bool) und Ring(bool) auslesen und labeln
#Bild rendern
#Bones zurückrotieren
#das ganze loopen

#def generateData():
    
