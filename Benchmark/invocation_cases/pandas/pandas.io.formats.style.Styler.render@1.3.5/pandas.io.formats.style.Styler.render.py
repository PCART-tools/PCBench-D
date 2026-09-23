import pandas as pd
import inspect
from pandas.io.formats.style import Styler

def main():
    df = pd.DataFrame({
        'A': [1, 2],
        'B': [3, 4]
    })
    styler = Styler(df)
    result = Styler.render(styler)
    print("render result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(Styler.render))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()