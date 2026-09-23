import torch
import inspect
from torch.jit.quantized import QuantizedLSTM

def main():
    input_size = 10
    hidden_size = 20
    num_layers = 2
    other = torch.nn.LSTM(
        input_size,
        hidden_size,
        num_layers
    )
    qlstm = QuantizedLSTM(other, torch.int8)

    print(type(qlstm))

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(QuantizedLSTM))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()