@needs_xelatex
@needs_ghostscript
def test_png():
    # Just a smoketest.
    fig, ax = plt.subplots()
    fig.savefig(BytesIO(), format="png", backend="pgf")
