import torch
import inspect

def main():
    # Create a random tensor
    A = torch.randn(3, 3)
    
    # Call the target API
    LU, pivots, info = torch.btrifact_with_info(A)
    print("LU decomposition:", LU)
    print("Pivots:", pivots)
    print("Info:", info)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(torch.btrifact_with_info))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()