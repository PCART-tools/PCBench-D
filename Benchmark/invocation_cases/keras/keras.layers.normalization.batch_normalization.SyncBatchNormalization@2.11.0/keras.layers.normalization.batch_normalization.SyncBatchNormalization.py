from keras.layers.normalization.batch_normalization import SyncBatchNormalization
from keras.models import Sequential
import numpy as np
import inspect

def main():
    input_data = np.random.rand(1, 10, 10, 3)

    model = Sequential()
    model.add(SyncBatchNormalization(input_shape=(10, 10, 3)))

    model.compile(optimizer='adam', loss='mse')
    result = model.predict(input_data)
    print("SyncBatchNormalization result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(SyncBatchNormalization))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
