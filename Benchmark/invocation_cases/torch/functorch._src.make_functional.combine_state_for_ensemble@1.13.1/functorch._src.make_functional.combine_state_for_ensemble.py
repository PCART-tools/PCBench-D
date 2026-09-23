import torch
import torch.nn as nn
import inspect
from functorch._src.make_functional import combine_state_for_ensemble

class DummyModel(nn.Module):
    def __init__(self, state, param):
        super(DummyModel, self).__init__()
        self.state = state
        self.param = nn.Parameter(param)

def main():
    # Simulate model states and parameters using DummyModel class
    models = [DummyModel(torch.randn(2, 2), torch.randn(2, 2)) for _ in range(3)]

    # Call the target API
    result = combine_state_for_ensemble(models)
    print("combine_state_for_ensemble result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(combine_state_for_ensemble))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()