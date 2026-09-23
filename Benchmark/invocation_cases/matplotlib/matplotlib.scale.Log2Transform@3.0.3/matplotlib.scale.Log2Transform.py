import matplotlib.scale as mscale
import inspect

def main():
    transform = mscale.Log2Transform()
    result = transform.transform([1, 2, 4, 8])
    print("Log2Transform result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(mscale.Log2Transform))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()