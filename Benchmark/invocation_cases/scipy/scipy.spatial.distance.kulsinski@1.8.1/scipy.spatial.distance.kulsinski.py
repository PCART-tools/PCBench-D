import scipy.spatial.distance as distance
import inspect

def main():
    u = [1, 0, 1, 1]
    v = [0, 1, 1, 1]
    result = distance.kulsinski(u, v)
    print("kulsinski result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(distance.kulsinski))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()