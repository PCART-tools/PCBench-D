import sympy
import inspect

def main():
    number = 31
    result = sympy.is_mersenne_prime(number)
    print("is_mersenne_prime result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(sympy.is_mersenne_prime))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()