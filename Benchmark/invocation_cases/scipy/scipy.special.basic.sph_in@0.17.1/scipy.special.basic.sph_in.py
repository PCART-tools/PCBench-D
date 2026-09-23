import scipy.special as sp
import inspect

def main():
    n = 2
    z = 1.0
    result = sp.sph_in(n, z)
    print("sph_in result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(sp.sph_in))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()