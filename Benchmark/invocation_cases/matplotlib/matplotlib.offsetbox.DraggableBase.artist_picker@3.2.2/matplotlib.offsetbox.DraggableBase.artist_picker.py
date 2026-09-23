import matplotlib
matplotlib.use("Agg")
import matplotlib.offsetbox as mob
import matplotlib.backend_bases as mbb
import matplotlib.pyplot as plt
import inspect

def main():
    fig, ax = plt.subplots()
    text = ax.text(0.5, 0.5, 'Draggable Text', ha='center', va='center')
    draggable = mob.DraggableBase(text)
    evt = mbb.MouseEvent(
        name='button_press_event',
        canvas=fig.canvas,
        x=100,
        y=100,
        button=1
    )
    result = draggable.artist_picker(text, evt)
    print("artist_picker result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(mob.DraggableBase.artist_picker))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()