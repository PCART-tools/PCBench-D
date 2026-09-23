import torch
import inspect
from torch.ao.quantization.fx.quantization_patterns import CopyNodeQuantizeHandler

def main():
    handler = CopyNodeQuantizeHandler(None, None)
    print("CopyNodeQuantizeHandler instance created:", handler)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(CopyNodeQuantizeHandler))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()