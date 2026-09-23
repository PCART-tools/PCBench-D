    @pytest.mark.parametrize("plotter", PLOT_LIST, ids=PLOT_IDS)
    @pytest.mark.parametrize("ndata", numlike_data, ids=numlike_ids)
    def test_plot_numlike(self, ax, plotter, ndata):
        counts = np.array([4, 6, 5])
        plotter(ax, ndata, counts)
        axis_test(ax.xaxis, ndata)
