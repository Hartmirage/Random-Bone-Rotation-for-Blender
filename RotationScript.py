import bpy
import math
import mathutils
import os
from random import randrange
from random import randint
from random import uniform
from datetime import datetime

#--------------------------------------- START OF [VARIABLES] ----------------------------------------------------------
#
#define all needed variables that are set by the user here 
NumberOfPoses = 1 #Number of wanted results 
StartAt = 0 #if script was run before and an enhancement of the dataset is wanted, set the index accordingly.
#if the dataset features the files 0 to 100 set the StartAt variable to 101.
Directory = 'D:/blender_projects/handscript/test' #Filepath in witch the output will be saved(windows)-------------------------WINDOWS FORMAT
#Directory = '/Users/Oliver/Documents/projektarbeit/Handv2mitscript/exports' #-----------------------------------------------------MAC FORMAT

#define all needed variables that are set by the script here
#booleans will be set via the script and will later be exported in the labels file
hasWatch = False
hasRing = False
hasSleeve = False
isLeftHand = False
#HandList is used to store objects of class Hand, which stores all the needed Data for one Hand in one Objekt
HandList = []
ImageFilePath = Directory + '/images' #directory where the images will be saved
LabelsFilePath = Directory + '/labels' #directory where the labelfiles will b saved
#--------------------------------------- END OF [VARIABLES] ----------------------------------------------------------

#--------------------------------------- START OF [PREPARATION] ----------------------------------------------------------
#
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
    #take the defined filepaths for export and make sure they exist(create them)
    createDirectory(Directory)
    #create additional directories inside the mainpath for pictures and labels
    createDirectory(LabelsFilePath)
    createDirectory(ImageFilePath)
    
#Object that stores the rig, clothes, watch, ring and the parent collection of a Hand
class Hand:
  def __init__(self, collection, watches, rings, clothes, rig):
    self.collection = collection
    self.watches = watches
    self.rings = rings
    self.clothes = clothes
    self.rig = rig

#returns Substring from startIndex to endIndex of a given string
def getSubString(string, startIndex, endIndex):
    returnString = ''
    for i in range(startIndex, endIndex):
        returnString += string[i]
    return returnString

#returns a collection with a given name ---- used to get the Watch, Ring and Clothes of the corresponding HandCollection
def getSubCollection(string):
    List = []
    for col in bpy.data.collections:
        if string in col.name:
            List.append(col)
    return List  #the Collections are returned as an Array so the Clothes can be switched via an index, or in the future Rings and Watches can be switched

#returns a Rig with a given name
def getRig(string):
    for rig in bpy.data.objects:
        if string in rig.name:
            return rig

#creates the Objects of Class Hand and stores them in the HandList
#-----looks for a collection that is named like CollectionHand1, Rig like Hand1Rig, Watch like Hand1Watch etc.
def initHands():
    for x in bpy.data.collections:
        if "CollectionHand" in x.name:
            Name = getSubString(x.name, len(x.name)-5, len(x.name))      #this gets a String like "Hand1" to find all collections and the rig starting with "Hand1"
            HandList.append(Hand(x,
                                    getSubCollection(Name + "Watch"),
                                    getSubCollection(Name + "Ring"),
                                    getSubCollection(Name + "Cloth"),
                                    getRig(Name + "Rig")))
                                    
#hides the collection for the renderer    
def hideHand(Hand):
    Hand.collection.hide_render = True
    for i in Hand.watches:
        i.hide_render = True
    for i in Hand.rings:
        i.hide_render = True
    for i in Hand.clothes:
        i.hide_render = True

#before the mainloop hide all hand collections
def hideAllHands():
    for x in HandList:
        hideHand(x)

#this method need to run before the main loop to prepare all the collections and directories
def init():    
    createDirectories()
    initHands()
    hideAllHands()
#--------------------------------------- END OF [PREPARATION] ----------------------------------------------------------

#--------------------------------------- START OF [MAIN LOOP] --------------------------------------------------------------
#

#unhides the Collection of the given Hand in the Viewport
def unhideOne(Hand):
    Hand.collection.hide_render = False  
    for i in Hand.watches:
        i.hide_render = False
    for i in Hand.rings:
        i.hide_render = False
    for i in Hand.clothes:
        i.hide_render = False
    #set isLeftHand bool here. used for export later
    ForeArmBone = Hand.rig.pose.bones[0].name
    side = getSubString(ForeArmBone, len(ForeArmBone) - 1, len(ForeArmBone))
    if 'l' in side:
        isLeftHand = True
    else:
        isLeftHand = False
        
    print(Hand.collection.name)

#hides/unhides clothes, ring and watch based on randomness, but makes sure only one of each or none is enabled
#sets the booleans for labelexport
def randomize(Hand):
    #hide all watches, rings and sleeves
    for x in Hand.watches:
        x.hide_render = True
    for x in Hand.rings:
        x.hide_render = True
    for x in Hand.clothes:
        x.hide_render = True
    
    #determines if the watch is shown or not
    numOfWatches = len(Hand.watches)
    randWatch = 0    
    if numOfWatches != 0:
        randWatch = randint(0, numOfWatches) 
    if randWatch != 0 and numOfWatches != 0:
        Hand.watches[randWatch - 1].hide_render = False
        hasWatch = True
        print(Hand.watches[randWatch - 1].name)
    else:
        hasWatch = False
        print("no Watch")
    
    #determines if the ring is shown or not
    numOfRings = len(Hand.rings)
    randRing = 0
    if numOfRings != 0:
        randRing = randint(0, numOfRings)
    if randRing != 0 and numOfRings != 0:
        Hand.rings[randRing - 1].hide_render = False
        hasRing = True
        print(Hand.rings[randRing - 1].name)
    else:
        hasRing = False
        print("no Ring")
    
    #determines if a sleeve is shown or not and which one of them    
    numOfClothes = len(Hand.clothes)
    randCloth = 0
    if numOfClothes != 0:
        randCloth = randint(0, numOfClothes)
    if randCloth != 0 and numOfClothes != 0:
        Hand.clothes[randCloth - 1].hide_render = False
        hasSleeve = True
        print(Hand.clothes[randCloth - 1].name)
    else:
        hasSleeve = False
        print("no Cloth")
    
#rotates a single bone within the limits of the constraint
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
        
#renders image and saves it at the given path at the top of the script
def renderImage(counter):
    bpy.context.scene.camera = bpy.data.objects["Camera"]
    path = ImageFilePath + '/' + str(counter) + '.png'
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    bpy.context.scene.render.filepath = path
    bpy.ops.render.render(write_still = 1)

#renders 2 images from the 2 leap cameras and saves them at the given path at the top of the script
def renderLeapImage(counter):
    bpy.context.scene.camera = bpy.data.objects["IRCamera_L"]
    path = ImageFilePath + '/' + str(counter) + 'l.png'
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    bpy.context.scene.render.filepath = path
    bpy.ops.render.render(write_still = 1)
    
    bpy.context.scene.camera = bpy.data.objects["IRCamera_R"]
    path2 = ImageFilePath + '/' + str(counter) + 'r.png'
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    bpy.context.scene.render.filepath = path2
    bpy.ops.render.render(write_still = 1)

#formats the float to supress 1*e10 etc. format
def formatFloat(float):
    return '{:.12f}'.format(float)

#writes name of bone, HeadLocationVector and TailLocationVector in txt file for each bone, then writes the defined booleans
def exportLabels(counter, Rig, HandCollection):
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
    f.write('hasWatch = ' + str(hasWatch) + '\n')
    f.write('hasRing = ' + str(hasRing) + '\n')
    f.write('hasSleeve = ' + str(hasSleeve) + '\n')
    f.write('isLeftHand = ' + str(isLeftHand) + '\n')
    f.close()  

#the main method
def loop():
    if StartAt < 0:
        print("StartAt has to be 0 or higher")
        return
    index = StartAt
    for index in range(StartAt, StartAt + NumberOfPoses):
        #get length of HandList
        temp = len(HandList)
        #get Random Index 0 <= n < Number of Hands
        HandIndex = randrange(temp)
        Hand = HandList[HandIndex]
        #unhide Hand, cloth, ring and watch in render
        unhideOne(Hand)
    
        #randomize ring, watch and clothes
        randomize(Hand)
        #rotate the Bones of the rig
        rotateBones(Hand.rig)
    
        #renderImage(index)
        renderLeapImage(index)
        exportLabels(index, Hand.rig, Hand.collection)
    
        resetBones(Hand.rig)
        #hide it again
        hideHand(Hand) 
        
        now = datetime.now()

        current_time = now.strftime("%H:%M:%S")
        print("Current Time = ", current_time)
        print('-----------------\n')
#--------------------------------------- END OF [MAIN LOOP] -----------------------------------------------------------------

#--------------------------------------- START OF [METHOD CALLS] ------------------------------------------------------------
#     
init()
loop()
print("___________script finished")
#--------------------------------------- END OF [METHOD CALLS] --------------------------------------------------------------