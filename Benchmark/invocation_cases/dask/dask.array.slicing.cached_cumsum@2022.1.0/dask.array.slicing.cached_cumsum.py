import dask.array as da
import inspect
from dask.array.slicing import cached_cumsum

def main():
    x = da.ones(10, chunks=5)
    chunk_sizes = x.chunks[0]
    cs = cached_cumsum(chunk_sizes)
    print("cached_cumsum result:", cs)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(cached_cumsum))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()