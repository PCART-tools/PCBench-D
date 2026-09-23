@pytest.mark.parametrize("fmt", ["png", "pdf", "ps", "eps", "svg"])
def test_imsave_fspath(fmt):
    plt.imsave(Path(os.devnull), np.array([[0, 1]]), format=fmt)
