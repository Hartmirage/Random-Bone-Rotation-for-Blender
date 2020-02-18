import bpy
import math
import mathutils
import os
from random import uniform

WantedHand = 5 #for Hand1 to Hand6
NumberOfPoses = 1 #Number of Renders and LabelFiles that will be created
StartAt = 0 #if script was run before and you just want a few extra
#Directory = 'D:/blender_projects/handscript/test' #Filepath in witch the output will be saved
Directory = '/Users/Oliver/Documents/projektarbeit/Handv2mitscript/exports' #(Mac)

#rigs 1 to 6 from the correspondent collection e.g. Hand2 ->  Rig_Hand_2
Rig1 = bpy.data.objects["Rig_Hand_1"]
Rig2 = bpy.data.objects["Rig_Hand_2"]
Rig3 = bpy.data.objects["Rig_Hand_3"]
Rig4 = bpy.data.objects["Rig_Hand_4"]
Rig5 = bpy.data.objects["Rig_Hand_5"]
Rig6 = bpy.data.objects["Rig_Hand_6"]

def activeRig(RigNumber):
    switcher = {
                1:Rig1,
                2:Rig2,
                3:Rig3,
                4:Rig4,
                5:Rig5,
                6:Rig6
             }
    return switcher.get(RigNumber,"Invalid Handnumber")

#anothe aproach to determin the active Rig ##############################TODO
def setActiveRig():
    for x in bpy.context.view_layer.objects:
        helpSetActiveRig(x.name)
        
        
def helpSetActiveRig(Hand_Rig):
    switcher = {
                'Rig_Hand_1':Rig1,
                'Rig_Hand_2':Rig2,
                'Rig_Hand_3':Rig3,
                'Rig_Hand_4':Rig4,
                'Rig_Hand_5':Rig5,
                'Rig_Hand_6':Rig6
                }
    ARig = switcher.get(Hand_Rig,"Invalid Rig")

#rotates a single bone within the limits of the constaint
def rotateBone(self):
    self.rotation_mode = 'XYZ'
    self.rotation_euler.rotate_axis('X', uniform(self.constraints[0].min_x, self.constraints[0].max_x))
    self.rotation_euler.rotate_axis('Y', uniform(self.constraints[0].min_y, self.constraints[0].max_y))
    self.rotation_euler.rotate_axis('Z', uniform(self.constraints[0].min_z, self.constraints[0].max_z))
    #print(self)

#does the single bone rotation for all bones that have a constraint
def rotateBones():
    for x in (ARig.pose.bones):
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
def resetBones():
    for x in (ARig.pose.bones):
        try:
            resetBone(x)
        except:
            pass
        
#rotates all bones, renders the image and resets the bones
def rotateAndRender(counter):
    rotateBones()
    print('____________________')

    renderImage(counter)
    
    exportLabels(counter)
    
    resetBones()

#renders image and saves it at the given path at the top of the script
def renderImage(counter):
    bpy.context.scene.camera = bpy.data.objects["Camera"]
    path = ImageFilePath + '/' + str(counter) + '.png'
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    bpy.context.scene.render.filepath = path
    bpy.ops.render.render(write_still = 1)

#formats the float to supress 1*e10 etc. format
def formatFloat(float):
    #return '{:.12f}'.format(round(float, roundLocationDoublesBy))
    return '{:.12f}'.format(float)

#writes name of bone, HeadLocationVector and TailLocationVector in txt file for each bone
def exportLabels(counter):
    path = LabelsFilePath + '/' + str(counter) + '.txt'
    f = open(str(path), 'w')
    for x in (ARig.pose.bones):
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

#setActiveRig() ###todo

#select ActiveRig according to the WantedHand at the start of the script
ARig = activeRig(WantedHand)

#set ARig to active Object to make sure that enabling Pose Mode is possible
bpy.context.view_layer.objects.active = ARig
#make sure to be in POSE mode, so the rotation will show in the rendered Image(in Object mode you won't see the difference)
bpy.ops.object.mode_set(mode='POSE')

#setting the Path Variables
FilePath = Directory + '/' + ARig.name
ImageFilePath = FilePath + '/images' #directory where the images will be saved
LabelsFilePath = FilePath + '/labels' #directory where the labelfiles will b saved

#creates needed Directorys
createDirectory(FilePath)
createDirectory(LabelsFilePath)
createDirectory(ImageFilePath)

#loop for the wanted number of images
for i in range(StartAt, StartAt + NumberOfPoses):
    rotateAndRender(i)
    print(i)
