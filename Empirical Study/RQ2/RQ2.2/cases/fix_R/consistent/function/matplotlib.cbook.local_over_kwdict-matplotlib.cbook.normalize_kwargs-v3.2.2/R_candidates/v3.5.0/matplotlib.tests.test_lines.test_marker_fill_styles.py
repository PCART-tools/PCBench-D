@image_comparison(['marker_fill_styles.png'], remove_text=True)
def test_marker_fill_styles():
    colors = itertools.cycle([[0, 0, 1], 'g', '#ff0000', 'c', 'm', 'y',
                              np.array([0, 0, 0])])
    altcolor = 'lightgreen'

    y = np.array([1, 1])
    x = np.array([0, 9])
    fig, ax = plt.subplots()

    for j, marker in enumerate(mlines.Line2D.filled_markers):
        for i, fs in enumerate(mlines.Line2D.fillStyles):
            color = next(colors)
            ax.plot(j * 10 + x, y + i + .5 * (j % 2),
                    marker=marker,
                    markersize=20,
                    markerfacecoloralt=altcolor,
                    fillstyle=fs,
                    label=fs,
                    linewidth=5,
                    color=color,
                    markeredgecolor=color,
                    markeredgewidth=2)

    ax.set_ylim([0, 7.5])
    ax.set_xlim([-5, 155])
