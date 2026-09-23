import torch
import functorch
import inspect

def main():
    def simple_function(x):
        return x ** 2

    x = torch.tensor(3.0, requires_grad=True)
    grad_fn = functorch.grad(simple_function)
    result = grad_fn(x)
    print("grad result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(functorch.grad))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()