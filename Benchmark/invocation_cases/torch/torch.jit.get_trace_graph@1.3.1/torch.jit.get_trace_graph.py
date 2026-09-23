import torch
import torch.nn as nn
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
    example_input = torch.rand(1, 2)

    # Trace the model
    trace, _ = torch.jit.get_trace_graph(model, example_input)
    print("Trace graph:", trace)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(torch.jit.get_trace_graph))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()