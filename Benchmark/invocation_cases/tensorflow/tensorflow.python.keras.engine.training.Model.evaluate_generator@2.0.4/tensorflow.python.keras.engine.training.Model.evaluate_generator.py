import tensorflow as tf
import numpy as np
import inspect

def main():
    # Create a simple model
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(10, activation='relu', input_shape=(20,)),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    x_train = np.random.random((100, 20))
    y_train = np.random.randint(2, size=(100, 1))
    model.fit(x_train, y_train, epochs=1, batch_size=10)
    def data_generator():
        while True:
            yield np.random.random((10, 20)), np.random.randint(2, size=(10, 1))

    result = tf.keras.Model.evaluate_generator(model,data_generator(), steps=10)
    print("evaluate_generator result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(tf.keras.Model.evaluate_generator))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()