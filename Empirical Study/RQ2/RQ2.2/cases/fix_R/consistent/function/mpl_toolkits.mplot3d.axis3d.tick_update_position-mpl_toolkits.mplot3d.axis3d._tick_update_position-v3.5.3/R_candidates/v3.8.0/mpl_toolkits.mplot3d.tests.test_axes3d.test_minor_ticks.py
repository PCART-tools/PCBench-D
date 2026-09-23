@image_comparison(["minor_ticks.png"], style="mpl20")
def test_minor_ticks():
    ax = plt.figure().add_subplot(projection="3d")
    ax.set_xticks([0.25], minor=True)
    ax.set_xticklabels(["quarter"], minor=True)
    ax.set_yticks([0.33], minor=True)
    ax.set_yticklabels(["third"], minor=True)
    ax.set_zticks([0.50], minor=True)
    ax.set_zticklabels(["half"], minor=True)
