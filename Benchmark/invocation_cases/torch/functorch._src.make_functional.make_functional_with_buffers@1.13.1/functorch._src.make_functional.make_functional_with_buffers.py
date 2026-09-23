import torch
import torch.nn as nn
from functorch import make_functional_with_buffers
import inspect

def main():
    # Define a simple model
    class SimpleModel(nn.Module):
        def __init__(self):
            super(SimpleModel, self).__init__()
            self.linear = nn.Linear(2, 2)
        
        def forward(self, x):
            return self.linear(x)

    model = SimpleModel()
    fmodel, params, buffers = make_functional_with_buffers(model)
    
    # Test data
    x = torch.tensor([[1.0, 2.0]])
    result = fmodel(params, buffers, x)
    print("make_functional_with_buffers result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(make_functional_with_buffers))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()