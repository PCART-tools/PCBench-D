import torch
import inspect
from torch.jit.quantized import QuantizedLinear

def main():
    other = torch.nn.Linear(3, 2, bias=True)
    qlinear = QuantizedLinear(other)
    print("-----getsource_output-----")
    try:
        print(inspect.getsource(QuantizedLinear))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()