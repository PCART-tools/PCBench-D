import torch
import inspect

def main():
    result = torch.is_deterministic()
    print("is_deterministic result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(torch.is_deterministic))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()