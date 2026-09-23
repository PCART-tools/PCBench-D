import torch
import inspect

def main():
    result = torch._utils.is_compiling()
    print("is_compiling result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(torch._utils.is_compiling))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()