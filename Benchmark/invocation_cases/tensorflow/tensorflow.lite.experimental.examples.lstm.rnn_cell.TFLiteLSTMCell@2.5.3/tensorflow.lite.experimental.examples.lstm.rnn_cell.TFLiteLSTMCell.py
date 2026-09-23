from tensorflow.lite.experimental.examples.lstm.rnn_cell import TFLiteLSTMCell
import inspect

def main():
    lstm_cell = TFLiteLSTMCell(
        num_units=3,
    )
    print("Output:", lstm_cell)
    print("-----getsource_output-----")
    try:
        print(inspect.getsource(TFLiteLSTMCell))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()