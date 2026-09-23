import plotly
import plotly.tools as tls
import inspect

def main():
    fig = tls.make_subplots(rows=2, cols=2)
    print("make_subplots result:", fig)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(tls.make_subplots))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()