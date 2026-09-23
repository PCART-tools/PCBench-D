import torch
import torch.nn as nn
import torch.ao.quantization as quantization
from torch.jit.quantized import QuantizedLSTMCell
import inspect

def main():

    float_cell = nn.LSTMCell(input_size=10, hidden_size=20)
    lstm_cell = QuantizedLSTMCell(float_cell)
    print("QuantizedLSTMCell instance created:", lstm_cell)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(QuantizedLSTMCell))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()