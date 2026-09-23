    @pytest.mark.parametrize("plotter", plotters)
    @pytest.mark.parametrize("xdata", fvalues, ids=fids)
    def test_mixed_type_exception(self, plotter, xdata):
        ax = plt.figure().subplots()
        with pytest.raises(TypeError):
            plotter(ax, xdata, [1, 2])
