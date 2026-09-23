import inspect
from sklearn.utils.fixes import delayed

def main():
    def sample_function(x):
        return x * x

    delayed_func = delayed(sample_function)
    result = delayed_func(5)
    print("delayed result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(delayed))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()