import torch
import inspect

def main():
    matrices = [torch.tensor([[1, 2], [3, 4]]), torch.tensor([[5, 6], [7, 8]]), torch.tensor([[9, 10], [11, 12]])]
    result = torch.chain_matmul(*matrices)
    print("chain_matmul result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(torch.chain_matmul))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()