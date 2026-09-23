import pandas as pd
import inspect
from pandas.io.formats.style import Styler

def main():
    df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    styler = Styler(df)
    result = Styler.applymap(styler,lambda x: 'color: red' if x > 2 else 'color: blue')
    print(result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(Styler.applymap))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()