import pandas as pd
import inspect

def main():
    data = {
        'ItemA': pd.DataFrame([[1, 2], [3, 4]], columns=['A', 'B']),
        'ItemB': pd.DataFrame([[5, 6], [7, 8]], columns=['A', 'B'])
    }
    panel = pd.Panel(data)
    swapped = panel.swapaxes('items', 'major_axis')
    print("swapaxes result:\n", swapped)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pd.Panel.swapaxes))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()