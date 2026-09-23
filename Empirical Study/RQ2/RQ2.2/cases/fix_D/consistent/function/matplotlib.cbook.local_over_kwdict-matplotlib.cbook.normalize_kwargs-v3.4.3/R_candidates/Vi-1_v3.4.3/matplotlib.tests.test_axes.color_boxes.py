def color_boxes(fig, axs):
    """
    Helper for the tests below that test the extents of various axes elements
    """
    fig.canvas.draw()

    renderer = fig.canvas.get_renderer()
    bbaxis = []
    for nn, axx in enumerate([axs.xaxis, axs.yaxis]):
        bb = axx.get_tightbbox(renderer)
        if bb:
            axisr = plt.Rectangle(
                (bb.x0, bb.y0), width=bb.width, height=bb.height,
                linewidth=0.7, edgecolor='y', facecolor="none", transform=None,
                zorder=3)
            fig.add_artist(axisr)
        bbaxis += [bb]

    bbspines = []
    for nn, a in enumerate(['bottom', 'top', 'left', 'right']):
        bb = axs.spines[a].get_window_extent(renderer)
        spiner = plt.Rectangle(
            (bb.x0, bb.y0), width=bb.width, height=bb.height,
            linewidth=0.7, edgecolor="green", facecolor="none", transform=None,
            zorder=3)
        fig.add_artist(spiner)
        bbspines += [bb]

    bb = axs.get_window_extent()
    rect2 = plt.Rectangle(
        (bb.x0, bb.y0), width=bb.width, height=bb.height,
        linewidth=1.5, edgecolor="magenta", facecolor="none", transform=None,
        zorder=2)
    fig.add_artist(rect2)
    bbax = bb

    bb2 = axs.get_tightbbox(renderer)
    rect2 = plt.Rectangle(
        (bb2.x0, bb2.y0), width=bb2.width, height=bb2.height,
        linewidth=3, edgecolor="red", facecolor="none", transform=None,
        zorder=1)
    fig.add_artist(rect2)
    bbtb = bb2
    return bbaxis, bbspines, bbax, bbtb
