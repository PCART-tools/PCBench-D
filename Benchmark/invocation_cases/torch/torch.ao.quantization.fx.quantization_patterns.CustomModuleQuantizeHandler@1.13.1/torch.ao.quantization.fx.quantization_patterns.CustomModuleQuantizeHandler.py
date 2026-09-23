import torch
import inspect
from torch.ao.quantization.fx.quantization_patterns import CustomModuleQuantizeHandler

def main():
    # Simulate a simple use case for CustomModuleQuantizeHandler
    node_pattern = None
    modules = {}
    handler = CustomModuleQuantizeHandler(
        node_pattern=node_pattern,
        modules=modules,
        is_custom_module=True
    )
    print("CustomModuleQuantizeHandler instance created:", handler)


    print("-----getsource_output-----")
    try:
        print(inspect.getsource(torch.ao.quantization.fx.quantization_patterns.CustomModuleQuantizeHandler))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()