import pandas as pd
import inspect

def main():
    s1 = pd.Series([1, 2, 3], index=['a', 'b', 'c'])
    s2 = pd.Series([4, 5, 6], index=['b', 'c', 'd'])
    aligned_s1, aligned_s2 = s1.align(s2)
    print("Aligned Series 1:\n", aligned_s1)
    print("Aligned Series 2:\n", aligned_s2)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pd.Series.align))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()