@needs_xelatex
@pytest.mark.style('default')
@pytest.mark.backend('pgf')
def test_pathclip():
    mpl.rcParams.update({'font.family': 'serif', 'pgf.rcfonts': False})
    plt.plot([0., 1e100], [0., 1e100])
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.savefig(BytesIO(), format="pdf")  # No image comparison.
