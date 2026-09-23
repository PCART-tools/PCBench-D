import torch
import inspect

def main():
    A = torch.randn(1, 3, 3)
    LU_data, pivots = torch.functional.btrifact(A)

    print("LU_data:", LU_data)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(torch.functional.btrifact))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()