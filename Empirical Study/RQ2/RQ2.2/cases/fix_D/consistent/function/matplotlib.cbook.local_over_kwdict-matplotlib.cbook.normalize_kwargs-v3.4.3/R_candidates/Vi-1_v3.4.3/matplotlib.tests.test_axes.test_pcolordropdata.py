@check_figures_equal(extensions=["png"])
def test_pcolordropdata(fig_test, fig_ref):
    ax = fig_test.subplots()
    x = np.arange(0, 10)
    y = np.arange(0, 4)
    np.random.seed(19680801)
    Z = np.random.randn(3, 9)
    # fake dropping the data
    ax.pcolormesh(x[:-1], y[:-1], Z[:-1, :-1], shading='flat')

    ax = fig_ref.subplots()
    # test dropping the data...
    x2 = x[:-1]
    y2 = y[:-1]
    with pytest.warns(MatplotlibDeprecationWarning):
        ax.pcolormesh(x2, y2, Z, shading='flat')
