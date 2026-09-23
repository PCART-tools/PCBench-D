import matplotlib.mathtext as mtext
import inspect

def main():
    neg_fill = mtext.NegFill()
    print("NegFill instance created:", neg_fill)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(mtext.NegFill))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()