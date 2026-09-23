import pandas as pd
import inspect

def main():
    data = {
        'Item1': pd.DataFrame({'A': [1, 2], 'B': [3, 4]}),
        'Item2': pd.DataFrame({'A': [5, 6], 'B': [7, 8]})
    }
    panel = pd.Panel(data)
    result = panel.pop('Item1')
    print("pop result:\n", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pd.Panel.pop))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()