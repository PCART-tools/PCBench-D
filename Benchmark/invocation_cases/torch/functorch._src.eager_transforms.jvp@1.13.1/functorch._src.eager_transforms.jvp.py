import torch
import functorch
import inspect

def main():
    def f(x):
        return x ** 2

    x = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)
    v = torch.tensor([1.0, 1.0, 1.0])

    result, _ = functorch.jvp(f, (x,), (v,))
    print("jvp result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(functorch.jvp))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()