import scipy.constants as constants
import inspect

def main():
    fahrenheit = 212
    celsius = constants.F2C(fahrenheit)
    print("F2C result:", celsius)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(constants.F2C))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()