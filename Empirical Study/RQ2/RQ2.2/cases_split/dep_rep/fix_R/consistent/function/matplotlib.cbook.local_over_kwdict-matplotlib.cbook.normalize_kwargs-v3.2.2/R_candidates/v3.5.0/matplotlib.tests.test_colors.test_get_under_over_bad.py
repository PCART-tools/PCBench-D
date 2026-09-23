def test_get_under_over_bad():
    cmap = plt.get_cmap('viridis')
    assert_array_equal(cmap.get_under(), cmap(-np.inf))
    assert_array_equal(cmap.get_over(), cmap(np.inf))
    assert_array_equal(cmap.get_bad(), cmap(np.nan))
