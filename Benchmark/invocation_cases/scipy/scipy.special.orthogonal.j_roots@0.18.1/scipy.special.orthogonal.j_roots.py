import scipy.special
import inspect

def main():
    n = 3
    alpha = 0.5
    beta = 0.5
    mu = False
    roots, weights = scipy.special.orthogonal.j_roots(n, alpha, beta, mu)
    print("j_roots result:", roots, weights)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(scipy.special.orthogonal.j_roots))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()