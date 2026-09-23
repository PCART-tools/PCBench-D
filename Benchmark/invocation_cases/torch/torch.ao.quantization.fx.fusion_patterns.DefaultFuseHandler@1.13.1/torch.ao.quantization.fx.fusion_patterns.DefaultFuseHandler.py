import torch
import inspect
from torch.ao.quantization.fx.fusion_patterns import DefaultFuseHandler
from torch.fx import symbolic_trace, GraphModule

def main():
    # Create a dummy module to trace
    class DummyModule(torch.nn.Module):
        def forward(self, x):
            return x

    dummy_model = DummyModule()
    traced = symbolic_trace(dummy_model)

    # Extract a node from the traced graph
    dummy_node = list(traced.graph.nodes)[0]
    
    # Create an instance of DefaultFuseHandler
    handler = DefaultFuseHandler(dummy_node)
    print("DefaultFuseHandler instance created:", handler)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(DefaultFuseHandler))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()