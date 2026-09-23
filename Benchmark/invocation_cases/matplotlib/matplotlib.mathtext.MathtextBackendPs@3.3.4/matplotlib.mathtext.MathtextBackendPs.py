import matplotlib.mathtext as mathtext
import inspect

def main():
    backend_ps = mathtext.MathtextBackendPs()
    print("MathtextBackendPs instance:", backend_ps)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(mathtext.MathtextBackendPs))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()