import bpy
import math
import mathutils
import os
from random import randrange
from random import uniform

#define all needed variables that are set by the user here
NumberOfPoses = 1 #Number of Renders and LabelFiles that will be created
StartAt = 0 #if script was run before and you just want a few extra
#Directory = 'D:/blender_projects/handscript/test' #Filepath in witch the output will be saved(windows)
Directory = '/Users/Oliver/Documents/projektarbeit/Handv2mitscript/exports' #(Mac)

#define all needed variables that are set by the script here
FilePath = ''
ImageFilePath = ''
LabelsFilePath = ''

hasWatch = False
hasRing = False
hasSleeve = False

ActiveCollection = bpy.data.collections["Hand 1"] #this is only done to set the right type
HandList = []

#call this before the mainloop
def createDirectories():
    #take the defined filepath for export and make sure it exists(create it)
    #create additional directories inside the mainpath for picutures and labels

def hideAllHands():
    #before the mainloop hide all hand collections

#call this inside the mainloop
def prepareHand():
    #choose one hand, set as active, unhide the collection of active hand
    #hide/unhide clothes, ring and watch (randomized)
    #rotate bones randomized within the limits of the constraints
    
#####insert all methods helping the prepare method underneath

def export():
    #export labels: right/left, hasWatch(bool), hasRing(bool), hasSleeve(bool)
    #export labels for each bone(position, rotation??)
    #render image and save
    #render tiefenbild?
    
#####insert all methods helping the export method underneath

def reset():
    #reset rotation of bones
    #hide the active hand collection

def mainloop():
    

class Hand:
  def __init__(self, collection, watch, ring, cloth1, cloth2, cloth3, rig):
    self.collection = collection
    self.watch = watch
    self.ring = ring
    self.cloth1 = cloth1
    self.cloth2 = cloth2
    self.cloth3 = cloth3
    self.rig = rig

def initHands():
    Hand1 = Hand(bpy.data.collections["Hand 1"],
                        bpy.data.collections["Watch Hand 1"],
                        bpy.data.collections["Ring Hand 1"],
                        bpy.data.collections["Cloth 1 Hand 1"],
                        bpy.data.collections["Cloth 2 Hand 1"],
                        bpy.data.collections["Cloth 3 Hand 1"],
                        bpy.data.objects["Rig_Hand_1"])
    HandList.append(Hand1)
    
    Hand2 = Hand(bpy.data.collections["Hand 2"],
                        bpy.data.collections["Watch Hand 2"],
                        bpy.data.collections["Ring Hand 2"],
                        bpy.data.collections["Cloth 1 Hand 2"],
                        bpy.data.collections["Cloth 2 Hand 2"],
                        bpy.data.collections["Cloth 3 Hand 2"],
                        bpy.data.objects["Rig_Hand_2"])
    HandList.append(Hand2)
    
    Hand3 = Hand(bpy.data.collections["Hand 3"],
                        bpy.data.collections["Watch Hand 3"],
                        bpy.data.collections["Ring Hand 3"],
                        bpy.data.collections["Cloth 1 Hand 3"],
                        bpy.data.collections["Cloth 2 Hand 3"],
                        bpy.data.collections["Cloth 3 Hand 3"],
                        bpy.data.objects["Rig_Hand_3"])
    HandList.append(Hand3)
    
    Hand4 = Hand(bpy.data.collections["Hand 4"],
                        None,
                        bpy.data.collections["Ring Hand 4"],
                        None,
                        None,
                        None,
                        bpy.data.objects["Rig_Hand_4"])
    HandList.append(Hand4)
    
    Hand5 = Hand(bpy.data.collections["Hand 5"],
                        bpy.data.collections["Watch Hand 5"],
                        bpy.data.collections["Ring Hand 5"],
                        bpy.data.collections["Cloth 1 Hand 5"],
                        bpy.data.collections["Cloth 2 Hand 5"],
                        bpy.data.collections["Cloth 3 Hand 5"],
                        bpy.data.objects["Rig_Hand_5"])
    HandList.append(Hand5
    )
    Hand6 = Hand(bpy.data.collections["Hand 6"],
                        bpy.data.collections["Watch Hand 6"],
                        bpy.data.collections["Ring Hand 6"],
                        bpy.data.collections["Cloth 1 Hand 6"],
                        bpy.data.collections["Cloth 2 Hand 6"],
                        None,
                        bpy.data.objects["Rig_Hand_6"])
    HandList.append(Hand6)

#returns the Hand Rig of the Hand Collection that is visible
def getActiveRig():
    for x in bpy.context.view_layer.objects:
        if x == bpy.data.objects["Rig_Hand_1"]:
            return x
        if x == bpy.data.objects["Rig_Hand_2"]:
            return x
        if x == bpy.data.objects["Rig_Hand_3"]:
            return x
        if x == bpy.data.objects["Rig_Hand_4"]:
            return x
        if x == bpy.data.objects["Rig_Hand_5"]:
            return x
        if x == bpy.data.objects["Rig_Hand_6"]:
            return x

def setActiveCollection(Rig):
    global ActiveCollection
    if Rig == bpy.data.objects["Rig_Hand_1"]:
        ActiveCollection = bpy.data.collections["Hand 1"]
    if Rig == bpy.data.objects["Rig_Hand_2"]:
        ActiveCollection = bpy.data.collections["Hand 2"]
    if Rig == bpy.data.objects["Rig_Hand_3"]:
        ActiveCollection = bpy.data.collections["Hand 3"]
    if Rig == bpy.data.objects["Rig_Hand_4"]:
        ActiveCollection = bpy.data.collections["Hand 4"]
    if Rig == bpy.data.objects["Rig_Hand_5"]:
        ActiveCollection = bpy.data.collections["Hand 5"]
    if Rig == bpy.data.objects["Rig_Hand_6"]:
        ActiveCollection = bpy.data.collections["Hand 6"]

def randomizeClothing(Collection):
    sleeve = randrange(5) #gets random integer between 0 and 4
    ring = randrange(2)
    watch = randrange(2)
    
    

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

#creates the Directory with a given path
def createDirectory(path):
    try:
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)

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
    
    
#main()
testing()

 
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

def generateData():
    
