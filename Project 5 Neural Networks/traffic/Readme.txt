In my first attempt, I used:

- 1 pair of convolutional layer and max pooling layer
- 1 flatten layer
- 2 dense layers

Training accuracy is 0.9683, val accuracy 0.8827. This is might be a sign of overfitting.



In my second attempt, I used:

- 2 pairs of convolutional layer and max pooling layer
- 1 flatten layer
- 1 dropout layer
- 3 dense layers. 

The result is pretty good having 0.9292 training accuracy and 0.9224 val accuracy.