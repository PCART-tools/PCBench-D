from tensorflow.lite.experimental.examples.lstm.rnn_cell import TfLiteRNNCell
import inspect

def main():
    rnn_cell = TfLiteRNNCell(
        num_units=10
    )
    print("SimpleRNNCell created:", rnn_cell)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(TfLiteRNNCell))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()