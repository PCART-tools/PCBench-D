    @pytest.mark.usefixtures("test_data")
    @pytest.mark.parametrize("plotter", PLOT_LIST, ids=PLOT_IDS)
    def test_plot_xaxis(self, ax, test_data, plotter):
        plotter(ax, self.x, self.xy)
        axis_test(ax.xaxis, self.x)
