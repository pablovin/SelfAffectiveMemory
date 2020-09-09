"""
Emotion Recognition - Vision-Frame-Based Face Channel

__author__ = "Pablo Barros"

__version__ = "0.1"
__maintainer__ = "Pablo Barros"
__email__ = "barros@informatik.uni-hamburg.de"

More information about the implementation of the model:

Barros, P., Churamani, N., & Sciutti, A. (2020). The FaceChannel: A Light-weight Deep Neural Network for Facial Expression Recognition. arXiv preprint arXiv:2004.08195.

Barros, P., & Wermter, S. (2016). Developing crossmodal expression recognition based on a deep neural model. Adaptive behavior, 24(5), 373-396.
http://journals.sagepub.com/doi/full/10.1177/1059712316664017

"""

import numpy
import cv2
from Utils import imageProcessingUtil, modelDictionary, modelLoader, GUIController
import os
import time
import AffectiveMemory


import csv

import tensorflow as tf
config = tf.ConfigProto()
config.gpu_options.allow_growth=True
sess = tf.Session(config=config)

affectiveMemory = AffectiveMemory.AffectiveMemory() # Affective Memory

loadVideosFrom = "/home/pablo/Documents/Datasets/wristbot/videos" #Folde where the videos are
saveCSVFiles = "/home/pablo/Documents/Datasets/wristbot/csvAffMem" #Folder that will hold the .csv files

modelDimensional = modelLoader.modelLoader(modelDictionary.DimensionalModel) #Load neural network

imageProcessing = imageProcessingUtil.imageProcessingUtil()

for videoDirectory in os.listdir(loadVideosFrom): #for each video inside this folder

    videoTime = time.time()  # start time of the loop

    cap = cv2.VideoCapture(loadVideosFrom+"/"+videoDirectory) #open the video

    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    """
    Opens the .csv file 
    """
    with open(saveCSVFiles+"/"+videoDirectory+".csv", mode='w') as employee_file:
        employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        employee_writer.writerow(['Frame', 'Arousal', 'Valence'])

        frameCount = 0

        fpsCounter = []
        print ("Started Video:" + str(videoDirectory) +" - Total Frames:" + str(total))
        while(cap.isOpened() and not frameCount == total): #for each frame in this video
            start_time = time.time()  # start time of the loop
            ret, frame = cap.read()
            frameCount = frameCount + 1
            # print ("Frame count:" + str(frameCount))
            if type(frame) is numpy.ndarray:
                facePoints, face = imageProcessing.detectFace(frame) #detect a face

                if not len(face) == 0:   # If a face is detected

                    face = imageProcessing.preProcess(face,imageSize=(64,64))     # pre-process the face

                    dimensionalRecognition = numpy.array(modelDimensional.classify(face))    # Obtain dimensional classification

                    # use arousal/valence as input to the affective memory
                    affectiveMemoryInput = numpy.array(dimensionalRecognition[:, 0, 0]).flatten()

                    # If affective memory is not built, build it.
                    if not affectiveMemory.isBuilt:
                        # print ("BUild")
                        affectiveMemory.buildModel(affectiveMemoryInput)
                    # if affective memory is already built, train it with the new facial expression
                    else:
                        # print("train")
                        affectiveMemory.train(affectiveMemoryInput)

                    affectiveMemoryNodes, affectiveMemoryNodesAges = affectiveMemory.getNodes()

                    arousal = numpy.array(affectiveMemoryNodes)[:, 0]
                    valence = numpy.array(affectiveMemoryNodes)[:, 1]
                    averageArousal = numpy.mean(arousal)
                    averageValence = numpy.mean(valence)

                else: #if there is no face
                    averageArousal = -99
                    averageValence = -99


                employee_writer.writerow([int(frameCount), averageArousal, averageValence])
                fpsCounter.append(1.0 / (time.time() - start_time))



    fpsAvg = numpy.array(fpsCounter).mean()
    videoTime =  (time.time() - videoTime)

    print("Finished Video: " + str(videoDirectory) +"- FPS:" + str(fpsAvg) + " - Time:" + str(videoTime) +" seconds")

    cap.release()
    cv2.destroyAllWindows()