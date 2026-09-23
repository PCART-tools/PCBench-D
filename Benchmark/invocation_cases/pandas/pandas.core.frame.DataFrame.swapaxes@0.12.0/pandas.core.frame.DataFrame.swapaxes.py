import pandas as pd
import inspect

def main():
    df = pd.DataFrame({
        'A': [1, 2, 3],
        'B': [4, 5, 6]
    })
    result = df.swapaxes(0, 1)
    print("swapaxes result:\n", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pd.DataFrame.swapaxes))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()