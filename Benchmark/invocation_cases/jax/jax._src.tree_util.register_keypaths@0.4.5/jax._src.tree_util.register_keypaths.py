import inspect
from jax._src.tree_util import register_keypaths

def handler(path):
    return path

def main():
    def subtree_fn(path, x):
        return handler(path)

    result = register_keypaths(dict, subtree_fn)
    print("register_keypaths result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(register_keypaths))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
