import sympy as sp
import inspect

def main():
    n = 30
    result = sp.primenu(n)
    print("primenu result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(sp.primenu))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()