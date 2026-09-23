import keras
from keras.layers import ThresholdedReLU

import numpy as np
import inspect

def main():
    # Create test data
    data = np.array([[-1.0, 0.0, 1.0, 2.0]])

    # Instantiate the ThresholdedReLU layer
    thresholded_relu_layer = ThresholdedReLU(theta=1.0)

    # Apply the layer to the test data
    result = thresholded_relu_layer(data)
    print("ThresholdedReLU result:", result.numpy())

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(ThresholdedReLU))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
