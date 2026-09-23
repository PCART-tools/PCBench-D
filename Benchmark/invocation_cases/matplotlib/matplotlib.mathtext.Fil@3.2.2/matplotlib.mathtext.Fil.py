import inspect
from matplotlib import mathtext

def main():
    fil = mathtext.Fil()
    print("Fil object:", fil)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(mathtext.Fil))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
