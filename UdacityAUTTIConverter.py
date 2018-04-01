import os
import pandas as pd
import math
import xml.etree.ElementTree as ET
from VOCConverter import ToVOCConverter

class UdacityAUTTItoVOCConverter(ToVOCConverter):
    '''
    Data from the Udacity nano degree for self driving car. This data is from AUTTI.
    Autti data, object-dataset.tar.gz:
        This dataset is similar to CrowdAI but contains additional fields for occlusion and an additional label for traffic lights. 
        The dataset was annotated entirely by humans using Autti and is slightly larger with 15,000 frames.
        The label file has no headers
        Labels: Car, Truck, Pedestrian, Street Lights

        CSV Format:
        *frame
        *xmin
        *ymin
        *xmax
        *ymax
        *occluded
        *label
        *attributes (Only appears on traffic lights)
    '''

    def __init__(self,imageFolder,sourceLabelFolder,outputLabelFolder):
        '''
        imageFolder: folder where all the images are
        sourceLabelFolder: File with the annotation file in it
        outputLabelFolder: path where ouptut files are to be saved
        '''
        super().__init__(imageFolder,sourceLabelFolder,outputLabelFolder)

        self.imageFormat = ".jpg"
        self.database = "Udacity ATTI"
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
        ET.SubElement(objectLabel,"occluded").text = str(objectLabelSeries.occluded)
        if type(objectLabelSeries.attributes) is str:
            ET.SubElement(objectLabel,"attributes").text = objectLabelSeries.attributes.lower()
        else:
            ET.SubElement(objectLabel,"attributes").text = ""
        

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
        col_names = ["Frame","xmin","ymin","xmax","ymax","occluded","Label","attributes"]
        data = pd.read_csv(sourceFile,names=col_names,delimiter=" ",engine="python")

        lableImageNames = data.Frame.tolist()
        lableImageNames = list(set(lableImageNames))

        # find all image files
        imageFiles = os.listdir(self.imageFolder)
        imageFileNames = [img for img in imageFiles if img.endswith(self.imageFormat)]

        # verify there is a label for each image and vise-a-versa
        imagesWithNoLabel = list(set(imageFileNames) - set(lableImageNames))
        labelsWithNoImage = list(set(lableImageNames) - set(imageFileNames))
        #assert len(imagesWithNoLabel) == 0, "Images with no label file found: {}".format(imagesWithNoLabel)
        if len(imagesWithNoLabel) != 0:
            print("Found {} images with no labels. It is possible that there is nothing in these images".format(len(imagesWithNoLabel)))
        assert len(labelsWithNoImage) == 0, "{} Labels with no image found: {}".format(len(labelsWithNoImage),labelsWithNoImage)

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


        
