import dask
import inspect

def main():
    # Set some options using set_options
    with dask.set_options(get=dask.get):
        print("set_options applied successfully.")

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(dask.set_options))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()