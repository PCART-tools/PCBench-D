import matplotlib.mathtext as mathtext
import inspect

def main():
    backend_svg = mathtext.MathtextBackendSvg()
    print("MathtextBackendSvg instance:", backend_svg)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(mathtext.MathtextBackendSvg))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()