import os
import xml.etree.ElementTree as ET
from VOCConverter import ToVOCConverter

imageFolder = "MITTest//images//"
labelIn = "MITTest//inputLabels//"
labelOut = "MITTest//outputLabels//"
#imageFolder = "/mnt/storage/Machine_Learning/Datasets/MIT_Street_Scenes/images"
#labelIn = "/mnt/storage/Machine_Learning/Datasets/MIT_Street_Scenes/Annotations/Anno_XML"
#labelOut = "MIT_VOC_Labels"

class MITtoVOCConverter(ToVOCConverter):
    '''
    MIT Street Scenes is in a similar format to Pascal VOC, but the labels are polygons not bounding boxes.
    Need to convert the polygons to bounding boxes and add in the additional required info.
    '''

    def __init__(self,imageFolder,sourceLabelFolder,outputLabelFolder):
        '''
        imageFolder: folder where all the images are
        sourceLabelFolder: path to folder where source data is saved
        outputLabelFolder: path where ouptut files are to be saved
        '''
        super().__init__(imageFolder,sourceLabelFolder,outputLabelFolder)

        self.imageFormat = ".JPG"
        self.database = "MIT Street Scenes"

    def createXMLLabelFile(self,labelFileName):
        '''
        Take in a MIT Street Scene label file for an image (labelFileName) and save out the Pascal VOC format label file
        Read in the existing XML and add to it
        '''
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

    def removeNewlines(self,root):
        '''
        The MIT street scenes XML has leading and trailing newlines on every entry, we are going to remove them to make everything cleaner
        '''
        for tag in root.iter():
            tag.text = tag.text.rstrip("\n").lstrip("\n")
        return root

    def convertDataset(self,verbose=False):
        '''
        Convert the entire dataset
        Note that for MIT we split the label name with a "_"
        '''

        # find all the label files
        labelFiles = os.listdir(self.sourceLabelFolder)
        numLabels = len(labelFiles)
        labelFileNames = [i.split("_")[0] for i in labelFiles]
        labelFileNames = list(set(labelFileNames))
        assert numLabels == len(labelFileNames), "Repeated label files!"

        # find all image files
        imageFiles = os.listdir(self.imageFolder)
        imageFileNames = [i.split(".")[0] for i in imageFiles]

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

converter = MITtoVOCConverter(imageFolder,labelIn,labelOut)
converter.convertDataset(verbose=True)


        
