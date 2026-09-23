def test_colorbarbase():
    # smoke test from #3805
    ax = plt.gca()
    Colorbar(ax, cmap=plt.cm.bone)
