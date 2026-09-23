import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText
from matplotlib.offsetbox import bbox_artist
import inspect

def main():
    fig, ax = plt.subplots()
    text = AnchoredText("Test", loc='upper left')
    ax.add_artist(text)
    
    # Create a bounding box for demonstration
    bbox = text.get_window_extent(fig.canvas.get_renderer())
    
    # Call bbox_artist
    result = bbox_artist(ax, bbox)
    print("bbox_artist result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(bbox_artist))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()