import torch
import inspect

def main():
    # Define a simple function to test custom_fwd
    @torch.cuda.amp.autocast_mode.custom_fwd
    def simple_function(x):
        return x * 2

    # Create a tensor and call the function
    tensor = torch.tensor([1.0, 2.0, 3.0], device='cuda')
    result = simple_function(tensor)
    print("custom_fwd result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(torch.cuda.amp.autocast_mode.custom_fwd))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()