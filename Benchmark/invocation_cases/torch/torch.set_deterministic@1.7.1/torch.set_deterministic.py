import torch
import inspect

def main():
    torch.set_deterministic(True)
    print("Deterministic mode set.")

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(torch.set_deterministic))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()