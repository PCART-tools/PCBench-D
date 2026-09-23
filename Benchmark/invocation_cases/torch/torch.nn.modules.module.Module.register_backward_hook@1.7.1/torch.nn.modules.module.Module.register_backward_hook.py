import torch
import inspect

def main():
    # Define a simple module
    class SimpleModule(torch.nn.Module):
        def __init__(self):
            super(SimpleModule, self).__init__()
            self.linear = torch.nn.Linear(2, 2)

        def forward(self, x):
            return self.linear(x)

    # Instantiate the module
    module = SimpleModule()

    # Define a backward hook function
    def backward_hook(module, grad_input, grad_output):
        print("Backward hook called")
        return grad_input

    # Register the backward hook
    hook_handle = module.register_backward_hook(backward_hook)

    # Create input tensor and perform forward and backward pass
    input_tensor = torch.tensor([[1.0, 2.0]], requires_grad=True)
    output = module(input_tensor)
    output.sum().backward()

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(module.register_backward_hook))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()