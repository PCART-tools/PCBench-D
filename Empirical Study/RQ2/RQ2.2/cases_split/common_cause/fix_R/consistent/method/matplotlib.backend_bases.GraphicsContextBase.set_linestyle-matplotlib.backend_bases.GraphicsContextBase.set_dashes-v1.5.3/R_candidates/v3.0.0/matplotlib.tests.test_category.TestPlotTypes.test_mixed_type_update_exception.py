    @pytest.mark.parametrize("plotter", PLOT_BROKEN_LIST, ids=PLOT_BROKEN_IDS)
    @pytest.mark.parametrize("xdata", fvalues, ids=fids)
    def test_mixed_type_update_exception(self, ax, plotter, xdata):
        with pytest.raises(TypeError):
            plotter(ax, [0, 3], [1, 3])
            plotter(ax, xdata, [1, 2])
