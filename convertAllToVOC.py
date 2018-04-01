'''
Convert multiple datasets 
'''
from KITTIConverter import KITTItoVOCConverter
from MITConverter import MITtoVOCConverter
from UdacityAUTTIConverter import UdacityAUTTItoVOCConverter
from UdacityCrowdAIConverter import UdacityCrowdAItoVOCConverter

# KITTI
#imageFolder = "KITTITest//images//"
#labelIn = "KITTITest//inputLabels//"
#labelOut = "KITTITest//outputLabels//"
imageFolder = "/mnt/storage/Machine_Learning/Datasets/KITTI/data_object_image_2/training/image_2"
labelIn = "/mnt/storage/Machine_Learning/Datasets/KITTI/data_object_label_2/training/label_2"
labelOut = "KITTI_VOC_Labels"
converter = KITTItoVOCConverter(imageFolder,labelIn,labelOut)
converter.convertDataset(verbose=True)

# MIT
#imageFolder = "MITTest//images//"
#labelIn = "MITTest//inputLabels//"
#labelOut = "MITTest//outputLabels//"
imageFolder = "/mnt/storage/Machine_Learning/Datasets/MIT_Street_Scenes/images"
labelIn = "/mnt/storage/Machine_Learning/Datasets/MIT_Street_Scenes/Annotations/Anno_XML"
labelOut = "MIT_VOC_Labels"
converter = MITtoVOCConverter(imageFolder,labelIn,labelOut)
converter.convertDataset(verbose=True)

#AUTTI
#imageFolder = "AUTTITest//images//"
#labelIn = "AUTTITest//inputLabels//"
#labelOut = "AUTTITest//outputLabels//"
imageFolder = "/mnt/storage/Machine_Learning/Datasets/Udacity_self_driving_car/object-dataset"
labelIn = "/mnt/storage/Machine_Learning/Datasets/Udacity_self_driving_car/object-dataset"
labelOut = "AUTTI_VOC_Labels"
converter = UdacityAUTTItoVOCConverter(imageFolder,labelIn,labelOut)
converter.convertDataset(verbose=True)

#CrowdAI
imageFolder = "/mnt/storage/Machine_Learning/Datasets/Udacity_self_driving_car/object-detection-crowdai"
labelIn = "CrowdAITest//inputLabels//"
labelOut = "CrowdAITest//outputLabels//"
#imageFolder = "/mnt/storage/Machine_Learning/Datasets/Udacity_self_driving_car/object-detection-crowdai"
#labelIn = "/mnt/storage/Machine_Learning/Datasets/Udacity_self_driving_car/object-detection-crowdai"
#labelOut = "CrowdAI_VOC_Labels"
converter = UdacityCrowdAItoVOCConverter(imageFolder,labelIn,labelOut)
converter.convertDataset(verbose=True)

