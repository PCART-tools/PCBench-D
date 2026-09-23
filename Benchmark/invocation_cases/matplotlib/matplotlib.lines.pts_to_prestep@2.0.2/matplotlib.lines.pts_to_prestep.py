import matplotlib.lines as mlines
import inspect

def main():
    x = [0, 1, 2, 3]
    y = [0, 1, 4, 9]
    result = mlines.pts_to_prestep(x, y)
    print("pts_to_prestep result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(mlines.pts_to_prestep))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()