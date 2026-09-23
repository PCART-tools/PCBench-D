import torch
import inspect

def main():
    tensor = torch.tensor([1, 2, 3, 4])
    result = torch.testing._core.make_non_contiguous(tensor)
    print("make_non_contiguous result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(torch.testing._core.make_non_contiguous))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()