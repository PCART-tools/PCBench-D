import matplotlib.mathtext as mtext
import inspect

def main():
    # Create an instance of NegFilll
    neg_fill = mtext.NegFilll()
    print("NegFilll instance created:", neg_fill)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(mtext.NegFilll))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()