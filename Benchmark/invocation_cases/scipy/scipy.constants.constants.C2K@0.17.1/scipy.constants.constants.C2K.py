import scipy.constants as const
import inspect

def main():
    celsius_temp = 25
    kelvin_temp = const.C2K(celsius_temp)
    print("Celsius to Kelvin:", kelvin_temp)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(const.C2K))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()