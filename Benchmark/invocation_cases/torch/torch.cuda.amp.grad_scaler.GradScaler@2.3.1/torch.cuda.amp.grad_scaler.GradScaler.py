import torch
import inspect

def main():
    scaler = torch.cuda.amp.GradScaler()
    print("GradScaler instance:", scaler)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(torch.cuda.amp.GradScaler))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()