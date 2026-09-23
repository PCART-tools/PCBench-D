import matplotlib.lines as mlines
import inspect

def main():
    x = [1, 2, 3, 4]
    y = [10, 20, 30, 40]
    result = mlines.pts_to_midstep(x, y)
    print("pts_to_midstep result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(mlines.pts_to_midstep))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()