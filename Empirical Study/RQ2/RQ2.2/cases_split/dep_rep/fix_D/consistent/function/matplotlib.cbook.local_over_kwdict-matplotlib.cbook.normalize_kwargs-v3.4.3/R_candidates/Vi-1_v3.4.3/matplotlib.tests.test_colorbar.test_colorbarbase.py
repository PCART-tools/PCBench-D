def test_colorbarbase():
    # smoke test from #3805
    ax = plt.gca()
    ColorbarBase(ax, cmap=plt.cm.bone)
