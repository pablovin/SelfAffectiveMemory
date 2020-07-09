**Affective Memory**

This repository holds the code for the Affective Memory:
A self-organizing and online model that learns specific characteristics of individual's
facial expressions.

**Train Model**

The Affective Memory is composed of two modules: a deep neural network, based on the [FaceChannel](https://github.com/pablovin/FaceChannel) neural network.

The Affective Memory is implemented as a Growing-When-Required network that learns online
how to map the arousals and valences from the [Face Channel](https://github.com/pablovin/FaceChannel) into a temporally-correlated reading.


**Webcam Demo**

![Screenshot](Images/Demo.gif)

The demo displays the current arousal/valence output coming from the [FaceChannel](https://github.com/pablovin/FaceChannel), and the
neurons learned by the affective memory. Each neuron is represented by a dot, and the brighter dot 
represents the newest neurons. The red dot represents the average arousal and valence readings.

Check the [video](https://youtu.be/KpBbicdQrMU).

****Requirements****

Install all the libraries on the requirements.txt file.


**Related Publications**

```sh
Barros, P., Barakova, E., & Wermter, S. (2020). Adapting the Interplay between Personalized and Generalized Affect Recognition based on an Unsupervised Neural Framework. IEEE Transactions on Affective Computing.
```

```sh
Barros, P., Parisi, G., & Wermter, S. (2019, May). A personalized affective memory model for improving emotion recognition. In International Conference on Machine Learning (pp. 485-494).
```


```sh
P. Barros, N. Churamani and A. Sciutti,  "The FaceChannel: A Light-Weight Deep Neural Network for Facial Expression Recognition.," in 2020 15th IEEE International Conference on Automatic Face and Gesture Recognition (FG 2020) (FG), Buenos Aires, undefined, AR, 2020 pp. 449-453.
doi: 10.1109/FG47880.2020.00070
keywords: {emotion recognition;deep learning}
url: https://doi.ieeecomputersociety.org/10.1109/FG47880.2020.00070
```

```sh
Barros, P., & Wermter, S. (2017, May). A self-organizing model for affective memory. In 2017 International Joint Conference on Neural Networks (IJCNN) (pp. 31-38). IEEE.
```

**License**

All the examples in this repository are distributed under the Creative Commons CC BY-NC-SA 3.0 DE license. If you use this corpus, you have to agree with the following itens:

- To cite our reference in any of your publication that make any use of these examples. The references are provided at the end of this page.
- To use this model for research purpose only.


**Contact**

Pablo Barros - pablo.alvesdebarros@iit.it




