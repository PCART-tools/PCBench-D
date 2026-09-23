import pandas as pd
import inspect
from pandas.io.formats.style import Styler

def main():
    df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    styler = df.style

    def highlight_max(s):
        return ['background-color: yellow' if v == max(s) else '' for v in s]

    result = Styler.applymap_index(styler,highlight_max, axis=0)
    print("applymap_index result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(Styler.applymap_index))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()