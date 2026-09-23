import pandas as pd
import inspect
from pandas.io.formats.style import Styler

def main():
    df = pd.DataFrame({'A': [1.12345, 2.67891], 'B': [3.14159, 4.98765]})
    styler = Styler(df)
    result = Styler.set_precision(styler,2)
    print(result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(Styler.set_precision))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()