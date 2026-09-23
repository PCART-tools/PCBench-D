import scipy.constants as const
import inspect

def main():
    kelvin_temp = 300
    celsius_temp = const.K2C(kelvin_temp)
    print("K2C result:", celsius_temp)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(const.K2C))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()