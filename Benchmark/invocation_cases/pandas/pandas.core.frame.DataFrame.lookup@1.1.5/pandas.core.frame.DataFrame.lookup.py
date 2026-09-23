import pandas as pd
import inspect

def main():
    df = pd.DataFrame({
        'A': [1, 2, 3],
        'B': [4, 5, 6]
    })
    row_labels = [0, 1, 2]
    col_labels = ['A', 'B', 'A']
    result = df.lookup(row_labels, col_labels)
    print("lookup result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pd.DataFrame.lookup))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()