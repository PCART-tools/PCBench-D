import inspect
from rich._ratio import ratio_divide

def main():
    total = 100
    ratios = [1, 2, 3]
    result = ratio_divide(total, ratios)
    print("ratio_divide result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(ratio_divide))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()