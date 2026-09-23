import pandas as pd
import inspect
from pandas.io.formats.style import Styler

def main():
    df = pd.DataFrame({
        'A': [1, 2, 3],
        'B': [4, 5, 6],
        'C': [7, 8, 9]
    })
    styler = Styler(df)
    result = Styler.hide_columns(styler,['B'])
    print("Styler with hidden columns:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(Styler.hide_columns))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()