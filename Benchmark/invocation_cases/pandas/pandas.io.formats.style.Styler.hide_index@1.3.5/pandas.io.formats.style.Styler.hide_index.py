import pandas as pd
import inspect
from pandas.io.formats.style import Styler

def main():
    # Create a sample DataFrame
    df = pd.DataFrame({
        'A': [1, 2, 3],
        'B': [4, 5, 6]
    })
    styler = Styler(df)

    result = Styler.hide_index(styler)
    print("Styler with hidden index:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(Styler.hide_index))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()