import keras
from keras.layers import EinsumDense
import numpy as np
import inspect

def main():
    # Define input data
    input_data = np.random.random((2, 3))
    
    # Create an EinsumDense layer
    layer = EinsumDense("ab,bc->ac", output_shape=(4,), bias_axes="c")
    
    # Call the layer on input data
    result = layer(input_data)
    print("EinsumDense result:", result.numpy())

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(EinsumDense))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()