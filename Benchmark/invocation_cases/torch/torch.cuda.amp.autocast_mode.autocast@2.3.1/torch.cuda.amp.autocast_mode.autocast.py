import torch
import inspect

def main():
    # Check if CUDA is available
    if torch.cuda.is_available():
        # Create a tensor and move it to the GPU
        x = torch.randn(3, 3, device='cuda')
        
        # Use autocast for mixed precision
        with torch.cuda.amp.autocast():
            y = x * 2.0
        print("Autocast result:", y)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(torch.cuda.amp.autocast))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()