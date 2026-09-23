    @pytest.mark.parametrize("plotter", PLOT_LIST, ids=PLOT_IDS)
    def test_StrCategoryLocatorPlot(self, plotter):
        ax = plt.figure().subplots()
        plotter(ax, [1, 2, 3], ["a", "b", "c"])
        np.testing.assert_array_equal(ax.yaxis.major.locator(), range(3))
