'''
Convert all the datasets to the darknet format for YOLO
'''

from VOCToDarknet import VOCToDarknet

# KIITI
imageFolder = "/mnt/storage/Machine_Learning/Datasets/KITTI/data_object_image_2/training/image_2"
sourceLabelFolder = "KITTI_Labels/VOCFormat/"
outputImageFile = "KITTI_Labels/imageList.txt"
outputLabelFolder = "KITTI_Labels/DarknetFormat/"
converter = VOCToDarknet(imageFolder,sourceLabelFolder,outputImageFile,outputLabelFolder)
converter.convertDataset()

#AUTTI
imageFolder = "/mnt/storage/Machine_Learning/Datasets/Udacity_self_driving_car/object-dataset"
sourceLabelFolder = "AUTTI_Labels/VOCFormat/"
outputImageFile = "AUTTI_Labels/imageList.txt"
outputLabelFolder = "AUTTI_Labels/DarknetFormat/"
converter = VOCToDarknet(imageFolder,sourceLabelFolder,outputImageFile,outputLabelFolder)
converter.convertDataset()

#CrowdAI
imageFolder = "/mnt/storage/Machine_Learning/Datasets/Udacity_self_driving_car/object-detection-crowdai"
sourceLabelFolder = "CrowdAI_Labels/VOCFormat/"
outputImageFile = "CrowdAI_Labels/imageList.txt"
outputLabelFolder = "CrowdAI_Labels/DarknetFormat/"
converter = VOCToDarknet(imageFolder,sourceLabelFolder,outputImageFile,outputLabelFolder)
converter.convertDataset()

#MIT Street Scenes
imageFolder = "/mnt/storage/Machine_Learning/Datasets/MIT_Street_Scenes/images"
sourceLabelFolder = "MIT_Labels/VOCFormat/"
outputImageFile = "MIT_Labels/imageList.txt"
outputLabelFolder = "MIT_Labels/DarknetFormat/"
converter = VOCToDarknet(imageFolder,sourceLabelFolder,outputImageFile,outputLabelFolder)
converter.convertDataset()




