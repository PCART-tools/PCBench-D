import torch
from functorch import vmap
import inspect

def main():
    def square(x):
        return x ** 2

    x = torch.tensor([1, 2, 3, 4])
    result = vmap(square)(x)
    print("vmap result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(vmap))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()