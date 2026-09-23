import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axis3d import move_from_center
import inspect


def main():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    result = move_from_center([1, 2, 3], [1, 1, 1], [0.5, 0.5, 0.5], [0.1, 0.1, 0.1])
    print("move_from_center result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(move_from_center))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()