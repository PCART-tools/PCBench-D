def test_xkcd_no_cm():
    assert mpl.rcParams["path.sketch"] is None
    plt.xkcd()
    assert mpl.rcParams["path.sketch"] == (1, 100, 2)
    gc.collect()
    assert mpl.rcParams["path.sketch"] == (1, 100, 2)
