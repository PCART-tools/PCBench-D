import pandas as pd
import inspect
from pandas.core.reshape import convert_dummies

def main():
    data = pd.DataFrame({
        'A': ['a', 'b', 'a'],
        'B': ['b', 'a', 'b'],
        'C': [1, 2, 3]   
    })

    result = convert_dummies(
        data=data,
        cat_variables=['A', 'B'],
        prefix_sep='_'
    )

    print("convert_dummies result:\n", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(convert_dummies))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
