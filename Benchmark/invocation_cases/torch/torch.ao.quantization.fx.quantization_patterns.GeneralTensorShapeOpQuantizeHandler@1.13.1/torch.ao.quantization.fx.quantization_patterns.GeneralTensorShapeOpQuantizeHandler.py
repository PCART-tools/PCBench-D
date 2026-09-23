import torch
from torch.fx import Graph
import inspect
from torch.ao.quantization.fx.quantization_patterns import (
    GeneralTensorShapeOpQuantizeHandler
)

def main():
    graph = Graph()
    x = graph.placeholder("x")
    y = graph.call_method("view", args=(x, -1))
    graph.output(y)
    node_pattern = y         
    modules = {}             
    handler = GeneralTensorShapeOpQuantizeHandler(
        node_pattern,
        modules,
    )
    print("Handler created:", handler)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(GeneralTensorShapeOpQuantizeHandler))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()