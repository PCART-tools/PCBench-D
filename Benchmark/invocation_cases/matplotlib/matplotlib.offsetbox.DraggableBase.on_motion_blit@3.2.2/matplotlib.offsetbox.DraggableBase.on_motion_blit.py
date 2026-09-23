import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.offsetbox import DraggableBase
import inspect

def main():
    fig, ax = plt.subplots()
    draggable = DraggableBase(ax)
    result = draggable.on_motion_blit(None)
    print("on_motion_blit result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(DraggableBase.on_motion_blit))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()