import tensorflow as tf
import numpy as np
import inspect

def main():
    # Create a simple model
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(10, activation='relu', input_shape=(20,)),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    
    # Compile the model
    model.compile(optimizer='adam', loss='binary_crossentropy')

    # Generate dummy data
    data = np.random.random((100, 20))
    labels = np.random.randint(2, size=(100, 1))

    # Fit the model
    model.fit(data, labels, epochs=1, batch_size=10)

    # Create a generator
    def data_generator():
        while True:
            yield np.random.random((10, 20))

    # Use predict_generator
    predictions = tf.keras.Model.predict_generator(model,data_generator(), steps=10)
    print("predict_generator result:", predictions)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(tf.keras.Model.predict_generator))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()