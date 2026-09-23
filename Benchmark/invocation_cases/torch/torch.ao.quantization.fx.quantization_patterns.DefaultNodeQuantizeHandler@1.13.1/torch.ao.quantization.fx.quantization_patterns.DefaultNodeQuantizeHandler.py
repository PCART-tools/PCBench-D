import torch
import torch.fx as fx
import inspect
from torch.ao.quantization.fx.quantization_patterns import DefaultNodeQuantizeHandler

class SimpleModule(torch.nn.Module):
    def forward(self, x):
        return x + 1

def main():
    model = SimpleModule()
    gm = fx.symbolic_trace(model)
    node_pattern = None
    for n in gm.graph.nodes:
        if n.op == "call_function":
            node_pattern = n
            break
    modules = dict(gm.named_modules())
    handler = DefaultNodeQuantizeHandler(node_pattern, modules)
    print("DefaultNodeQuantizeHandler instance created:", handler)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(DefaultNodeQuantizeHandler))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()