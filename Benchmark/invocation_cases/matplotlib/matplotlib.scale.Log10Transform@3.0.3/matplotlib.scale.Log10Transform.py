import matplotlib.scale as mscale
import inspect

def main():
    log_transform = mscale.Log10Transform()
    result = log_transform.transform([1, 10, 100])
    print("Log10Transform result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(mscale.Log10Transform))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()