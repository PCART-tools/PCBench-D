import pandas as pd
import inspect
from pandas.io.formats.style import Styler

def main():
    # Create a sample DataFrame
    df = pd.DataFrame({
        'A': [1, None, 3],
        'B': [4, 5, None]
    })

    styler = Styler(df)
    result = Styler.set_na_rep(styler,'Missing')
    print(result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(Styler.set_na_rep))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()