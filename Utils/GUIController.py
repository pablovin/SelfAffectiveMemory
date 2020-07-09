import numpy
import cv2
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg


class GUIController:



    def createDetectedFacGUI(self, frame, detectedFace, modelDictionary=None, categoricalClassificationReport=[]):


        faceColor = (0,0,0)

        # Draw Detected Face
        for (x, y, w, h) in detectedFace:
            cv2.rectangle(frame, (x, y), (w, h), faceColor, 2)


        return frame


    def createDimensionalEmotionGUI(self, classificationReport, frame, categoricalReport=[], categoricalDictionary=None):



        if not len(categoricalReport) == 0:

            mainClassification = numpy.argmax(categoricalReport)
            pointColor = categoricalDictionary.classesColor[mainClassification]
        else:
            pointColor = (255,255,255)


        #Dimensional Report

        cv2.line(frame, (640+170, 70), (640+170, 270), (255, 255, 255), 4)
        cv2.line(frame, (640+85, 170), (640+285, 170), (255, 255, 255), 4)

        cv2.putText(frame, "Excited", (640+150, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(frame, "Calm", (640+150,290), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        cv2.putText(frame, "Negative", (640+15, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(frame, "Positive", (640+295, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        arousal = 1-float(float(classificationReport[0][0][0]) * 100)
        valence = float(float(classificationReport[1][0][0]) * 100)

        #print "Arousal:", arousal
        #print "Valence:", valence

        #arousal,valence
        cv2.circle(frame, (640+185+int(valence), 170+int(arousal)), 5, pointColor, -1)


        return frame


    def createCategoricalEmotionGUI(self, classificationReport, frame, modelDictionary, initialPosition=0):


        classificationReport = classificationReport*100


        for index,emotion in enumerate(modelDictionary.classsesOrder):

            emotionClassification = int(classificationReport[int(index)])

            cv2.putText(frame, emotion, (640+5, initialPosition+15+int(index)*20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,  modelDictionary.classesColor[index], 1)

            cv2.rectangle(frame, (640+100, initialPosition+5+int(index)*20), (int(640+100 + emotionClassification), initialPosition+20+int(index)*20), modelDictionary.classesColor[index], -1)
            cv2.putText(frame, str(emotionClassification) + "%", (int(640+105 + emotionClassification + 10), initialPosition+20+int(index)*20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, modelDictionary.classesColor[index], 1)

        return frame



    def createAffectiveMemoryGUI(self, affectiveMemoryWeights, affectiveMemoryNodesAges, frame):

        valence  = numpy.array(affectiveMemoryWeights)[:,0]
        arousal = numpy.array(affectiveMemoryWeights)[:, 1]
        numberNeurons = len(affectiveMemoryWeights)

        # habituatedArousals = []
        # habituatedValences = []
        # for a in range(len(affectiveMemoryWeights)):
        #     habituatedArousals.append(arousal[a] * float(a/len(affectiveMemoryWeights)))
        #     habituatedValences.append(valence[a] * float(a/len(affectiveMemoryWeights)))

        averageArousal = numpy.mean(arousal)
        averageValence = numpy.mean(valence)

        # print ("Arousals:" + str(arousal))
        # print ("Valences:" + str(valence))
        # print ("Average Arousal valence:"  + str(averageArousal)+","+str(averageValence))
        # print ("-------------")

        # print ("Mood age:" + str(affectiveMemoryNodesAges))

        figure = plt.figure()
        plot = figure.add_subplot(111)
        canvas = FigureCanvasAgg(figure)

        plt.scatter(arousal, valence, c = affectiveMemoryNodesAges, cmap='viridis')# With color
        # plot.scatter(arousal, valence, alpha=affectiveMemoryNodesAges, c="r") # without color

        for index, a in enumerate(arousal):
            # print ("Index:" + str(index))
            plot.scatter(a, valence[index], alpha=float(index/len(arousal)), c="b") # without color

        plot.scatter(averageArousal,averageValence, c="red")


        plot.set_xlim(-1, 1)
        plot.set_ylim(-1, 1)
        plot.set_xlabel('Arousal')
        plot.set:ylabel('Valence')

        canvas.draw()
        image = canvas.buffer_rgba()
        image = numpy.asarray(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # convert to a NumPy array
        # image = np.asarray(buf)
        #
        #
        # image = fig2data(figure)
        # plt.savefig("/home/pablo/Documents/Workspace/SelfAffectiveMemory/test2.png")
        # plt.clf()
        # cv2.imwrite("/home/pablo/Documents/Workspace/SelfAffectiveMemory/test.png", image)

        # plt.savefig(
        #     "tmpPlot.png")
        #
        #
        #
        # image = numpy.array(cv2.imread("tmpPlot.png"))

        image = cv2.resize(image, (380,380))

        # print ("Shape Image:", image.shape)
        # print("Shape Image:", frame.shape)

        frame[388:768, 644:1024] = image

        cv2.putText(frame, "Affective Memory" , (660 , 328 + 15), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (255,255,255), 1)
        cv2.putText(frame, "Neurons: " + str(numberNeurons), (660, 368 + 15), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (255, 255, 255), 1)


        return frame