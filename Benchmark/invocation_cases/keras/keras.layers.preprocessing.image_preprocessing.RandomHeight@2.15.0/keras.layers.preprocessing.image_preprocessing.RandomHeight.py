import keras
from keras.layers import RandomHeight

import inspect
import numpy as np

def main():
    # Simulate input data
    input_data = np.random.rand(1, 100, 100, 3).astype(np.float32)

    # Create RandomHeight layer
    random_height_layer = RandomHeight(factor=(0.2, 0.5))

    # Apply the layer to the input data
    result = random_height_layer(input_data)
    print("RandomHeight result shape:", result.shape)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(RandomHeight))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
