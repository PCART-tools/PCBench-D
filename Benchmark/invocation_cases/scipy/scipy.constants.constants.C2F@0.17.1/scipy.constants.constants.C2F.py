import scipy.constants as const
import inspect

def main():
    celsius_temp = 100.0
    fahrenheit_temp = const.C2F(celsius_temp)
    print("C2F result:", fahrenheit_temp)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(const.C2F))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()