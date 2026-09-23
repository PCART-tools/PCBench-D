import torch
from torch.cpu.amp.grad_scaler import GradScaler
import inspect

def main():
    scaler = GradScaler()
    print("GradScaler instance:", scaler)


    print("-----getsource_output-----")
    try:
        print(inspect.getsource(GradScaler))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()