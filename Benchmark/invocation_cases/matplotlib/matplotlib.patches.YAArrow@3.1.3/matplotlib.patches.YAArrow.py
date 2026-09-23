import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import inspect

def main():
    fig, ax = plt.subplots()
    arrow = mpatches.YAArrow(
        figure=fig,
        xytip=(200, 200), 
        xybase=(100, 100),  
        width=6,
        frac=0.2,
        headwidth=15,
        color="black"
    )

    print(arrow)
    print("-----getsource_output-----")
    try:
        print(inspect.getsource(mpatches.YAArrow))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()