import tensorflow as tf
import inspect

def main():
    # Simulate a simple model for mixed precision
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(10, activation='relu', input_shape=(10,))
    ])
    
    # Set optimizer before enabling mixed precision
    optimizer = tf.keras.optimizers.Adam()
    model.compile(optimizer=optimizer, loss='mse')

    # Enable mixed precision
    mixed_precision = tf.train.experimental.enable_mixed_precision_graph_rewrite(optimizer)
    print("Mixed precision enabled:", mixed_precision)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(tf.train.experimental.enable_mixed_precision_graph_rewrite))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()