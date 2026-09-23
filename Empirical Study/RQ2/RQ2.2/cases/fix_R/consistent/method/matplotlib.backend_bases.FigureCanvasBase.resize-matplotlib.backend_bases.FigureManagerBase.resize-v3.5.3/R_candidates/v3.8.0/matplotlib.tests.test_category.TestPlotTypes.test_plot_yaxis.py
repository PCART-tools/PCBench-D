    @pytest.mark.usefixtures("test_data")
    @pytest.mark.parametrize("plotter", PLOT_LIST, ids=PLOT_IDS)
    def test_plot_yaxis(self, test_data, plotter):
        ax = plt.figure().subplots()
        plotter(ax, self.yx, self.y)
        axis_test(ax.yaxis, self.y)
