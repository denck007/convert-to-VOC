import os
import pandas as pd
import xml.etree.ElementTree as ET
from VOCConverter import ToVOCConverter

imageFolder = "CrowdAITest//images//"
labelIn = "CrowdAITest//inputLabels//"
labelOut = "CrowdAITest//outputLabels//"
#imageFolder = "/mnt/storage/Machine_Learning/Datasets/MIT_Street_Scenes/images"
#labelIn = "/mnt/storage/Machine_Learning/Datasets/MIT_Street_Scenes/Annotations/Anno_XML"
#labelOut = "MIT_VOC_Labels"

class UdacityCrowdAItoVOCConverter(ToVOCConverter):
    '''
    Data from the Udacity nano degree for self driving car. This data is from CrowdAI.
        CrowdAI data, object-detection-crowdai.tar.gz:
        *The dataset includes driving in Mountain View California and neighboring cities during daylight conditions. 
        *It contains over 65,000 labels across 9,423 frames collected from a Point Grey research cameras running at full resolution of 1920x1200 at 2hz. 
        *The dataset was annotated by CrowdAI using a combination of machine learning and humans.
        *Labels in dataset: Car, Truck, Pedestrian

        Data is in 1 CSV. Each row is a label, so multiple rows per image. 
        Not going to keep the preview URL because they do not work. 
        Locations are in integer pixels.
        CSV Format:
        xmin
        ymin
        xmax
        ymax
        frame
        label
        preview url for frame 
    '''

    def __init__(self,imageFolder,sourceLabelFolder,outputLabelFolder):
        '''
        imageFolder: folder where all the images are
        sourceLabelFolder: File with the annotation file in it
        outputLabelFolder: path where ouptut files are to be saved
        '''
        super().__init__(imageFolder,sourceLabelFolder,outputLabelFolder)

        self.imageFormat = ".jpg"
        self.database = "Udacity CrowdAI"

    def createXMLLabelFile(self,labelDataFrame):
        '''
        Take in a pandas dataframe with all the labels for an image
        Generate the xml label for the image
        


        self.currentOutFile = os.path.join(self.outputLabelFolder,labelFileName[:labelFileName.rfind("_")] + ".xml")
        self.currentImageFile = labelFileName[:labelFileName.rfind("_")] + self.imageFormat

        labelXML = self.initializeXMLFile()

        sourceTree = ET.parse(os.path.join(self.sourceLabelFolder,labelFileName))
        sourceRoot = sourceTree.getroot()
        sourceRoot = self.removeNewlines(sourceRoot)

        # add the original source data to the new source data, purely to preserve data
        labelXML.find("source").extend(sourceRoot.find("source"))

        for objET in sourceRoot.iterfind("object"):
            objectLabel = self.createXMLLabel(objET)
            labelXML.append(objectLabel)

        tree = ET.ElementTree(labelXML)
        tree.write(self.currentOutFile)

        '''

    def createXMLLabel(self,objectLabel):
        '''
        Create a xml style label for the line that is passed in. Return the xml data
        '''

        # go over every "pt" label in the object and find the min/max values

        xmin = self.currentImageShape[0]
        xmax = 0
        ymin = self.currentImageShape[1]
        ymax = 0

        try:
            for pt in objectLabel.find("polygon").iterfind("pt"):
                x = pt.find("x").text.rstrip("\n").lstrip("\n")
                x = int(x)
                y = pt.find("y").text.rstrip("\n").lstrip("\n")
                y = int(y)

                xmin = min(xmin,x)
                xmax = max(xmax,x)
                ymin = min(ymin,y)
                ymax = max(ymax,y)

            bndbox = ET.SubElement(objectLabel,"bndbox")
            ET.SubElement(bndbox,"xmin").text = str(xmin)
            ET.SubElement(bndbox,"ymin").text = str(ymin)
            ET.SubElement(bndbox,"xmax").text = str(xmax)
            ET.SubElement(bndbox,"ymax").text = str(ymax)
        except:
            print("Error creating polygons for image :{}".format(self.currentImageFile))

        return objectLabel

    def convertDataset(self,verbose=False):
        '''
        Convert the entire dataset
        '''

        # read in the csv to pandas
        sourceFile = os.path.join(self.sourceLabelFolder,"labels.csv")
        assert os.path.exists(sourceFile), "There must be a labels.csv file in the sourceLabelFolder!"
        data = pd.read_csv(sourceFile,header=0)

        # find all image files
        imageFiles = os.listdir(self.imageFolder)
        imageFileNames = [i if i.contains(self.imageFormat) for i in imageFiles]


        # verify there is a label for each image and vise-a-versa
        imagesWithNoLabel = list(set(imageFileNames) - set(labelFileNames))
        labelsWithNoImage = list(set(labelFileNames) - set(imageFileNames))
        assert len(imagesWithNoLabel) == 0, "Images with no label file found: {}".format(imagesWithNoLabel)
        assert len(labelsWithNoImage) == 0, "Labels with no image found: {}".format(labelsWithNoImage)

        # call createXMLLabelFile() on each file
        counter = 0
        for label in labelFiles:
            counter += 1
            self.createXMLLabelFile(label)
            if verbose and counter%100==0:
                print("On image {}/{} {:.1f}% complete".format(counter,numLabels,float(counter)/float(numLabels)*100.))
        print("Finished converting {} labels!".format(numLabels))

converter = UdacityCrowdAItoVOCConverter(imageFolder,labelIn,labelOut)
converter.convertDataset(verbose=True)


        
