@image_comparison(['text_contains.png'])
def test_contains():
    fig = plt.figure()
    ax = plt.axes()

    mevent = MouseEvent('button_press_event', fig.canvas, 0.5, 0.5, 1, None)

    xs = np.linspace(0.25, 0.75, 30)
    ys = np.linspace(0.25, 0.75, 30)
    xs, ys = np.meshgrid(xs, ys)

    txt = plt.text(
        0.5, 0.4, 'hello world', ha='center', fontsize=30, rotation=30)
    # uncomment to draw the text's bounding box
    # txt.set_bbox(dict(edgecolor='black', facecolor='none'))

    # draw the text. This is important, as the contains method can only work
    # when a renderer exists.
    fig.canvas.draw()

    for x, y in zip(xs.flat, ys.flat):
        mevent.x, mevent.y = plt.gca().transAxes.transform([x, y])
        contains, _ = txt.contains(mevent)
        color = 'yellow' if contains else 'red'

        # capture the viewLim, plot a point, and reset the viewLim
        vl = ax.viewLim.frozen()
        ax.plot(x, y, 'o', color=color)
        ax.viewLim.set(vl)
