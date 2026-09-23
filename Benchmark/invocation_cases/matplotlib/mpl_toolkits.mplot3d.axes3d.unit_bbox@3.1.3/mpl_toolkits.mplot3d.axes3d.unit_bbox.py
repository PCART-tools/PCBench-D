import inspect
from mpl_toolkits.mplot3d.axes3d import unit_bbox

def main():
    result = unit_bbox()
    print(result)
    print("-----getsource_output-----")
    try:
        print(inspect.getsource(unit_bbox))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()