import scipy.signal.windows as windows
import inspect

def main():
    # Call the target API
    window = windows.slepian(10, width=0.5)
    print("slepian result:", window)

    # Get the source code of the target API
    print("-----getsource_output-----")
    try:
        print(inspect.getsource(windows.slepian))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()