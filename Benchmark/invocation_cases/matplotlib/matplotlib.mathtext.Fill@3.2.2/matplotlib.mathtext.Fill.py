import matplotlib.mathtext as mathtext
import inspect

def main():
    # Create a Fill object
    fill = mathtext.Fill()
    print("Fill object created:", fill)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(mathtext.Fill))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()