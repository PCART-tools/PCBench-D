    @pytest.mark.parametrize("plotter", PLOT_LIST, ids=PLOT_IDS)
    def test_StrCategoryLocatorPlot(self, ax, plotter):
        ax.plot(["a", "b", "c"])
        np.testing.assert_array_equal(ax.yaxis.major.locator(), range(3))
