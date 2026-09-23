from mpl_toolkits.axisartist.axislines import SimpleChainedObjects
import inspect

def main():
    obj = SimpleChainedObjects(None)

    print("SimpleChainedObjects instance:", obj)
    print("-----getsource_output-----")
    try:
        print(inspect.getsource(SimpleChainedObjects))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()