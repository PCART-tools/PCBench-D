import inspect
import torch
from torch.jit.quantized import QuantizedGRU

def main():
    torch.manual_seed(0)
    input_size = 10
    hidden_size = 20
    num_layers = 2
    seq_len = 3
    batch_size = 5
    float_gru = torch.nn.GRU(
        input_size=input_size,
        hidden_size=hidden_size,
        num_layers=num_layers,
        bias=True,
        batch_first=False,
        dropout=0.0,
        bidirectional=False,
    )
    qgru = QuantizedGRU(
        float_gru,
        dtype=torch.int8,
    )
    x = torch.randn(seq_len, batch_size, input_size)
    h0 = torch.randn(num_layers, batch_size, hidden_size)
    output, hn = qgru(x, h0)

    print("output shape:", output.shape)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(QuantizedGRU))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()