import torch
import inspect
from functorch import make_functional

def main():
    model = torch.nn.Linear(2, 2)
    fmodel, params = make_functional(model)
    print("make_functional result:", fmodel, params)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(make_functional))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()