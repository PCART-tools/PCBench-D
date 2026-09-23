import scipy.constants as const
import inspect

def main():
    fahrenheit = 32
    kelvin = const.F2K(fahrenheit)
    print("F2K result:", kelvin)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(const.F2K))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()