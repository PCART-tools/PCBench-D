import matplotlib.mathtext as mathtext
import inspect

def main():
    backend = mathtext.MathtextBackendCairo()
    print("MathtextBackendCairo instance:", backend)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(mathtext.MathtextBackendCairo))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()