import scipy.special
import inspect

def main():
    n = 2
    x = 1.0
    result = scipy.special.sph_yn(n, x)
    print("sph_yn result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(scipy.special.sph_yn))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()