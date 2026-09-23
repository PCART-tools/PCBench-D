import inspect
import torch
from torch.jit.quantized import QuantizedGRUCell

def main():
    torch.manual_seed(0)

    input_size = 10
    hidden_size = 20
    batch_size = 5
    float_cell = torch.nn.GRUCell(
        input_size=input_size,
        hidden_size=hidden_size,
        bias=True,
    )

    qgru = QuantizedGRUCell(
        float_cell
    )
    print(qgru)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(QuantizedGRUCell))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()