@image_comparison(['tight_layout_offsetboxes1', 'tight_layout_offsetboxes2'])
def test_tight_layout_offsetboxes():
    # 1.
    # - Create 4 subplots
    # - Plot a diagonal line on them
    # - Surround each plot with 7 boxes
    # - Use tight_layout
    # - See that the squares are included in the tight_layout
    #   and that the squares in the middle do not overlap
    #
    # 2.
    # - Make the squares around the right side axes invisible
    # - See that the invisible squares do not affect the
    #   tight_layout
    rows = cols = 2
    colors = ['red', 'blue', 'green', 'yellow']
    x = y = [0, 1]

    def _subplots():
        _, axs = plt.subplots(rows, cols)
        axs = axs.flat
        for ax, color in zip(axs, colors):
            ax.plot(x, y, color=color)
            add_offsetboxes(ax, 20, color=color)
        return axs

    # 1.
    axs = _subplots()
    plt.tight_layout()

    # 2.
    axs = _subplots()
    for ax in (axs[cols-1::rows]):
        for child in ax.get_children():
            if isinstance(child, AnchoredOffsetbox):
                child.set_visible(False)

    plt.tight_layout()
