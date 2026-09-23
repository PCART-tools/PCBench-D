import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import inspect

def main():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_frame_on(True)
    print("set_frame_on called successfully.")

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(Axes3D.set_frame_on))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()