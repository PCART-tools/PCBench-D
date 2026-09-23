import keras
from keras.layers import RandomWidth

import inspect
import numpy as np

def main():
    # Simulate input data
    input_data = np.random.rand(1, 100, 100, 3).astype(np.float32)
    # Batch of 1 image, 100x100 with 3 channels

    # Create a RandomWidth layer
    random_width_layer = RandomWidth(factor=0.2)

    # Apply the layer to the input data
    result = random_width_layer(input_data)
    print("RandomWidth result shape:", result.shape)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(RandomWidth))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
