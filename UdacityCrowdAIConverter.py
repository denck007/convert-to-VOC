import os
import pandas as pd
import xml.etree.ElementTree as ET
from VOCConverter import ToVOCConverter

#imageFolder = "CrowdAITest//images//"
#labelIn = "CrowdAITest//inputLabels//"
#labelOut = "CrowdAITest//outputLabels//"
imageFolder = "/mnt/storage/Machine_Learning/Datasets/Udacity_self_driving_car/object-detection-crowdai"
labelIn = "/mnt/storage/Machine_Learning/Datasets/Udacity_self_driving_car/object-detection-crowdai"
labelOut = "CrowdAI_VOC_Labels"

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
        self.labelSourceFileName = "labels.csv"

    def createXMLLabelFile(self,labelDataFrame):
        '''
        Take in a pandas dataframe with all the labels for an image
        Generate the xml label for the image
        '''
        self.currentImageFile = labelDataFrame.Frame[labelDataFrame.axes[0][0]]

        self.currentOutFile = os.path.join(self.outputLabelFolder,self.currentImageFile[:self.currentImageFile.rfind(self.imageFormat)] + ".xml")
        labelXML = self.initializeXMLFile()

        for label in labelDataFrame.itertuples():
            objectLabel = self.createXMLLabel(label)
            labelXML.append(objectLabel)

        tree = ET.ElementTree(labelXML)
        tree.write(self.currentOutFile)

        

    def createXMLLabel(self,objectLabelSeries):
        '''
        Create a xml style label for the dataframe that is passed in. Return the xml data
        '''

        objectLabel = ET.Element("object")
        ET.SubElement(objectLabel,"name").text = objectLabelSeries.Label

        bndbox = ET.SubElement(objectLabel,"bndbox")
        ET.SubElement(bndbox,"xmin").text = str(objectLabelSeries.xmin)
        ET.SubElement(bndbox,"ymin").text = str(objectLabelSeries.ymin)
        ET.SubElement(bndbox,"xmax").text = str(objectLabelSeries.xmax)
        ET.SubElement(bndbox,"ymax").text = str(objectLabelSeries.ymax)

        return objectLabel

    def convertDataset(self,verbose=False):
        '''
        Convert the entire dataset
        '''

        # read in the csv to pandas
        sourceFile = os.path.join(self.sourceLabelFolder,self.labelSourceFileName)
        assert os.path.exists(sourceFile), "There must be a {} file in the sourceLabelFolder!".format(self.labelSourceFileName)
        data = pd.read_csv(sourceFile,header=0)
        lableImageNames = data.Frame.tolist()
        lableImageNames = list(set(lableImageNames))

        # find all image files
        imageFiles = os.listdir(self.imageFolder)
        imageFileNames = [img for img in imageFiles if img.endswith(self.imageFormat)]

        # verify there is a label for each image and vise-a-versa
        imagesWithNoLabel = list(set(imageFileNames) - set(lableImageNames))
        labelsWithNoImage = list(set(lableImageNames) - set(imageFileNames))
        #assert len(imagesWithNoLabel) == 0, "Images with no label file found: {}".format(imagesWithNoLabel)
        if len(imagesWithNoLabel) == 0:
            print("Found {} images with no labels. It is possible that there is nothing in these images".format(len(imagesWithNoLabel)))
        assert len(labelsWithNoImage) == 0, "Labels with no image found: {}".format(labelsWithNoImage)

        numLabels = len(imageFileNames)
        # call createXMLLabelFile() on each file
        counter = 0
        for img in lableImageNames:
            counter += 1
            label = data[data.Frame == img]
            self.createXMLLabelFile(label)
            if verbose and counter%100==0:
                print("On image {}/{} {:.1f}% complete".format(counter,numLabels,float(counter)/float(numLabels)*100.))
        print("Finished converting {} labels!".format(numLabels))

converter = UdacityCrowdAItoVOCConverter(imageFolder,labelIn,labelOut)
converter.convertDataset(verbose=True)


        
