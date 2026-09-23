import pandas as pd
import inspect

def main():
    data = {
        'Item1': pd.DataFrame([[1, 2], [3, 4]], columns=['A', 'B']),
        'Item2': pd.DataFrame([[5, 6], [7, 8]], columns=['A', 'B'])
    }
    panel = pd.Panel(data)
    result = panel.keys()
    print("Panel keys:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pd.Panel.keys))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()