import tensorflow as tf
import inspect

def main():
    # Simulate input data
    num_units = 128
    lstm_cell = tf.contrib.rnn.LSTMCell(num_units)
    print("LSTMCell:", lstm_cell)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(tf.contrib.rnn.LSTMCell))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()