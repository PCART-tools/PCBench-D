import torch
import inspect

def main():
    # Check if CUDA is available
    if torch.cuda.is_available():
        result = torch.backends.cuda.sdp_kernel()
        print("sdp_kernel result:", result)
    else:
        print("CUDA is not available.")

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(torch.backends.cuda.sdp_kernel))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()