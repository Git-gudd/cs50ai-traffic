This is a homework project from CS50's Introduction to Artificial Intelligence, including pre existing specifications and guidelines as shown on the website https://cs50.harvard.edu/ai/2020/projects/5/traffic/.

In this project, I used TensorFlow to build a neural network to classify road signs based on an image of those signs in order to recognize and distinguish road signs – stop signs, speed limit signs, yield signs, and more. For this project, I used the German Traffic Sign Recognition Benchmark (GTSRB) dataset, which contains thousands of images of 43 different kinds of road signs. 

The goal for my traffic model is to reach good accuracy rate with a low loss rate. I started with only 1 convolution and pooling process and a hidden layer with a few nodes. The model only got 64% accuracy rate and 66% loss rate. Over the next multiple runs, where I changed the parameters, I have summarized a few key points:

    The change that worked well:
        Increasing the number of nodes in the hidden layer

        Increasing the size of the convolution's filter

        Increasing the number of convolution and pooling process
    
    The change that didn't work well:
        Increasing the number of hidden layers

        Increasing the number of filters in the convolution process did not improve the performance

        Increasing/Decreasing the dropout rate does seem to affect the performance, but not much, and the model might run the risk of overfitting.

In my final code, I decided to fix my parameters to:

    1. Convolution layer: 16 (5x5) filters
    2. Pooling layer: (2x2) pool size
    3. Convolution layer: 32 (5x5) filters
    4. Pooling layer: (2x2) pool size
    5. Flatten
    6. Hidden layer: 100 nodes
    7. Dropout: 0.5

and got an accuracy rate of 94.25% with a loss rate of 1.17%
