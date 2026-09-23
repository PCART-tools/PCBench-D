    @pytest.mark.parametrize("ydata", cases, ids=ids)
    @pytest.mark.parametrize("plotter", PLOT_LIST, ids=PLOT_IDS)
    def test_StrCategoryFormatterPlot(self, ax, ydata, plotter):
        plotter(ax, range(len(ydata)), ydata)
        for i, d in enumerate(ydata):
            assert ax.yaxis.major.formatter(i, i) == _to_str(d)
        assert ax.yaxis.major.formatter(i+1, i+1) == ""
        assert ax.yaxis.major.formatter(0, None) == ""
