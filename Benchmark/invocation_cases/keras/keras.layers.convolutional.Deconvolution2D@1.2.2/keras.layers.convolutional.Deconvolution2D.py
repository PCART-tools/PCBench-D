from keras.layers import Deconvolution2D
from keras.models import Sequential
import numpy as np
import inspect

def main():
    input_data = np.random.random((1, 3, 3, 1))

    model = Sequential()
    model.add(Deconvolution2D(
        nb_filter=1,
        nb_row=2,
        nb_col=2,
        output_shape=(1, 4, 4, 1),
        input_shape=(3, 3, 1)
    ))
    model.compile(optimizer='sgd', loss='mse')
    result = model.predict(input_data)
    print("Deconvolution2D result shape:", result.shape)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(Deconvolution2D))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
