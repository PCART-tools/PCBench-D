import torch
import torch.nn as nn
from torch.fx import symbolic_trace
from torch.ao.quantization.fx.quantization_patterns import BatchNormQuantizeHandler
import inspect


class M(nn.Module):
    def __init__(self):
        super().__init__()
        self.bn = nn.BatchNorm2d(3)

    def forward(self, x):
        return self.bn(x)


def main():
    model = M()
    gm = symbolic_trace(model)
    bn_node = None
    for node in gm.graph.nodes:
        if node.op == "call_module" and node.target == "bn":
            bn_node = node
            break
    modules = dict(gm.named_modules())
    handler = BatchNormQuantizeHandler(
        node_pattern=bn_node,
        modules=modules,
    )
    print(handler)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(BatchNormQuantizeHandler))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()