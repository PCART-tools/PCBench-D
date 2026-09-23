import torch
import torch.nn as nn
from torch.nn.utils.stateless import functional_call
import inspect

def main():
    # Define a simple model
    class SimpleModel(nn.Module):
        def __init__(self):
            super(SimpleModel, self).__init__()
            self.linear = nn.Linear(2, 2)

        def forward(self, x):
            return self.linear(x)

    # Instantiate the model and create input data
    model = SimpleModel()
    input_data = torch.tensor([[1.0, 2.0], [3.0, 4.0]])

    # Create a state dictionary with new parameters
    new_state_dict = {'linear.weight': torch.tensor([[1.0, 0.0], [0.0, 1.0]]),
                      'linear.bias': torch.tensor([0.0, 0.0])}

    # Call functional_call
    result = functional_call(model, new_state_dict, input_data)
    print("functional_call result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(functional_call))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()