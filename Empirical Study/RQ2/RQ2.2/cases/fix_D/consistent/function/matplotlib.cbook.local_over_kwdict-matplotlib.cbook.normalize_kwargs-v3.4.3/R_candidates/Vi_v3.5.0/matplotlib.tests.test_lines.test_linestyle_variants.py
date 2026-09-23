def test_linestyle_variants():
    fig, ax = plt.subplots()
    for ls in ["-", "solid", "--", "dashed",
               "-.", "dashdot", ":", "dotted"]:
        ax.plot(range(10), linestyle=ls)
    fig.canvas.draw()
