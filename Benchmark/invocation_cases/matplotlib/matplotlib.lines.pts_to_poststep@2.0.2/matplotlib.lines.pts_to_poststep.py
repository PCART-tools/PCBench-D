import matplotlib.lines as mlines
import inspect

def main():
    x = [0, 1, 2, 3]
    y = [0, 1, 0, 1]
    result = mlines.pts_to_poststep(x, y)
    print("pts_to_poststep result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(mlines.pts_to_poststep))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()