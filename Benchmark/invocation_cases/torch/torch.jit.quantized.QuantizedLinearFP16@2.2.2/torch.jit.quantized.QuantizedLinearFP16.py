import torch
import inspect
from torch.jit.quantized import QuantizedLinearFP16

def main():
    float_linear = torch.nn.Linear(3, 2, bias=True)
    float_linear.eval()
    qlinear_fp16 = QuantizedLinearFP16(float_linear)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(QuantizedLinearFP16))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()