import torch
import inspect

def main():
    x = torch.randn(3, 3, device='cpu')
    with torch.cpu.amp.autocast():
        result = x * 2
    print("autocast result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(torch.cpu.amp.autocast))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()