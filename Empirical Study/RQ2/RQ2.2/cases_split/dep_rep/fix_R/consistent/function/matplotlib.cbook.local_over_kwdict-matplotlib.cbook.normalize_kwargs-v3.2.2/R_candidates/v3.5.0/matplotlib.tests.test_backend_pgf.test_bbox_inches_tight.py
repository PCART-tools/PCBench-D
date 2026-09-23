@needs_xelatex
def test_bbox_inches_tight():
    fig, ax = plt.subplots()
    ax.imshow([[0, 1], [2, 3]])
    fig.savefig(BytesIO(), format="pdf", backend="pgf", bbox_inches="tight")
