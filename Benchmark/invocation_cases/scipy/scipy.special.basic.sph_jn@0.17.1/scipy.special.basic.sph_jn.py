import scipy.special as sp
import inspect

def main():
    n = 2
    x = 1.0
    result = sp.sph_jn(n, x)
    print("sph_jn result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(sp.sph_jn))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()