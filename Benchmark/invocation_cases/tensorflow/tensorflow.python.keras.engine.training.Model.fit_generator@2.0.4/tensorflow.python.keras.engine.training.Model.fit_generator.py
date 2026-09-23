import tensorflow as tf
import numpy as np
import inspect

def main():
    # Create a simple generator for demonstration
    def data_generator():
        while True:
            yield np.random.random((10, 3)), np.random.random((10, 1))

    # Define a simple model
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(10, activation='relu', input_shape=(3,)),
        tf.keras.layers.Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')

    # Use fit_generator
    result = tf.keras.Model.fit_generator(model,data_generator(), steps_per_epoch=1, epochs=1)
    print("fit_generator result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(tf.keras.Model.fit_generator))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()