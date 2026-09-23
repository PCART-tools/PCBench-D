import scipy.special as sp
import inspect

def main():
    n = 2
    z = 1.5
    result = sp.sph_kn(n, z)
    print("sph_kn result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(sp.sph_kn))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()