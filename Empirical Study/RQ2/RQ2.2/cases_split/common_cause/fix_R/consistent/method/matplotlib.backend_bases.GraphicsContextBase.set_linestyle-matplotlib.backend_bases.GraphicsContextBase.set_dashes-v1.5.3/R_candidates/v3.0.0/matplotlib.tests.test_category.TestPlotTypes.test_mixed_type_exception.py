    @pytest.mark.parametrize("plotter", PLOT_BROKEN_LIST, ids=PLOT_BROKEN_IDS)
    @pytest.mark.parametrize("xdata", fvalues, ids=fids)
    def test_mixed_type_exception(self, ax, plotter, xdata):
        with pytest.raises(TypeError):
            plotter(ax, xdata, [1, 2])
