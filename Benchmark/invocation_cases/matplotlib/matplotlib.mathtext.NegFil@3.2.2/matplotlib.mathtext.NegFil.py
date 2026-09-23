import matplotlib.mathtext as mathtext
import inspect

def main():
    # Instantiate NegFil to ensure the call is made to the target API
    neg_fil = mathtext.NegFil()
    print("NegFil instance created:", neg_fil)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(mathtext.NegFil))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()