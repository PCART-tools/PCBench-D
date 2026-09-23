import sympy
from sympy.vector import CoordSysCartesian
import inspect

def main():
    N = CoordSysCartesian('N')
    print("CoordSysCartesian name:", N.__str__())

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(CoordSysCartesian))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()