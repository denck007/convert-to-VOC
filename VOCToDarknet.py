import os
import xml.etree.ElementTree as ET
from time import time

class VOCToDarknet(object):
    '''
    Convert all the VOC style labels to a single text file that we can use in YOLO
    '''

    def __init__(self,imageFolder,sourceLabelFolder,outputImageFile,outputLabelFolder):
        '''
        imageFolder: folder where all the images are
        sourceLabelFolder: path to folder where source data is saved
        outputImageFile: Output file where all the images and paths will be listed
        outputLabelFolder: path where ouptut files are to be saved
        '''

        assert os.path.isdir(imageFolder), "Image folder {:} does not exist!".format(imageFolder)
        assert os.path.isdir(sourceLabelFolder), "Source label folder {:} does not exist!".format(sourceLabelFolder)
        assert os.path.isdir(outputLabelFolder), "Output label folder {:} does not exist!".format(outputLabelFolder)

        self.imageFolder = imageFolder
        self.sourceLabelFolder = sourceLabelFolder
        self.outputImageFile = outputImageFile
        self.outputLabelFolder = outputLabelFolder
        self.currentOutFile = None
        self.currentImageFile = None

        self.images = os.listdir(self.imageFolder)
        self.labels = os.listdir(self.sourceLabelFolder)


        self.truncatedMin = 0.
        self.truncatedMax = 1.
        self.difficultMin = 0.
        self.difficultMax = 1.
        self.sizeMin = 0. # minimum size in the width or height of the bounding box., is a [0,1] float as % of image size
        self.classes = ["car","pedestrian","truck"]

    def convertDataset(self):
        '''
        Convert all the label files
        '''
        self.writeImageNames()
        startTime = time()
        counter = 0
        for labelFile in self.labels:
            counter += 1
            print("\rConverting labels for image {}/{}".format(counter,len(self.labels)),end="")
            self.convertXML(os.path.join(self.sourceLabelFolder,labelFile))
        print("\nCompleted conversion in {:.1f} seconds".format(time()-startTime))

    def writeImageNames(self):
        '''
        Write all the image names to the outputImageFile
        '''
        with open(self.outputImageFile,"w") as f:
            for img in self.images:
                f.write(os.path.join(self.imageFolder,img)+"\n")

    def convertXML(self,fname):
        '''
        convert an entire VOC xml label file to the darknet style
        fname is the file name of the VOC xml file
        '''
        tree=ET.parse(fname)
        root = tree.getroot()
        imageFileName = root.find("filename").text
        size = root.find("size")
        w = float(size.find("width").text)
        h = float(size.find("height").text)

        outputFile = os.path.join(self.outputLabelFolder,imageFileName)
        outputFile = outputFile[:outputFile.rfind(".")]+".txt"
        with open(outputFile,"w") as f:
            for label in root.iter("object"):
                
                convertedLabel = self.convertLabel(label,(w,h))
                if type(convertedLabel) is str:
                    f.write(convertedLabel)

    def convertLabel(self,label,imgSize):
        '''
        Convert a single label
        label is a single tag of <object> in the xml file
        image size is a tuple of (width,height)
        '''
        if label.find("name") is not None: # check if there is actually a label
            labelClass = label.find("name").text.lower()
        else: 
            return None # this is an empty label
        if label.find("difficult") is not None:
            difficult = float(label.find("difficult").text)
        else:
            difficult = 0.
        if label.find("truncated") is not None:
            truncated = float(label.find("truncated").text)
        else:
            truncated = 0.
        
        bndBox = label.find("bndbox")
        xmin = float(bndBox.find("xmin").text)
        xmax = float(bndBox.find("xmax").text)
        ymin = float(bndBox.find("ymin").text)
        ymax = float(bndBox.find("ymax").text)

        dw = 1./imgSize[0]
        dh = 1./imgSize[1]
        x = dw*(xmin + xmax)/2.
        y = dh*(ymin + ymax)/2.
        w = dw*(xmax-xmin)
        h = dh*(ymax-ymin)

        if self.checkLabel(labelClass,difficult,truncated,w,h):
            labelIdx = self.classes.index(labelClass)
            return "{} {} {} {} {}\n".format(labelIdx,x,y,w,h)
        else: return None

    def checkLabel(self,labelClass,difficult,truncated,w,h):
        '''
        Verify that we want this label
        '''
        # Is it a class we want
        if labelClass not in self.classes:
            return False
        if difficult > self.difficultMax or difficult < self.difficultMin:
            return False
        if truncated > self.truncatedMax or truncated < self.truncatedMin:
            return False
        if w < self.sizeMin or h < self.sizeMin:
            return False
        
        # if it made it this far all conditions are met and return true
        return True
