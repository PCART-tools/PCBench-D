import scipy.constants as const
import inspect

def main():
    kelvin_temp = 273.15
    fahrenheit_temp = const.K2F(kelvin_temp)
    print("K2F result:", fahrenheit_temp)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(const.K2F))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()