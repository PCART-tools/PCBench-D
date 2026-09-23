import pandas as pd
import inspect

def main():
    data = [1.1, 2.2, 3.3, 4.4]
    index = pd.Float64Index(data)
    print("Float64Index:", index)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pd.Float64Index))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()