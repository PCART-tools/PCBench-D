import matplotlib.pyplot as plt
from matplotlib.axis import Axis
import inspect

class MyAxis(Axis):
    __name__ = 'myaxis'
    axis_name = 'my'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pass

    def _get_tick(self, major):
        pass

def main():
    fig, ax = plt.subplots()

    my_axis = MyAxis(
        axes=ax,
    )

    my_axis.cla()
    print("Axis cla called successfully.")

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(my_axis.cla))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()