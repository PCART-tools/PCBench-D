    @pytest.mark.parametrize("plotter", PLOT_LIST, ids=PLOT_IDS)
    @pytest.mark.parametrize("bdata", bytes_data, ids=bytes_ids)
    def test_plot_bytes(self, ax, plotter, bdata):
        counts = np.array([4, 6, 5])
        plotter(ax, bdata, counts)
        axis_test(ax.xaxis, bdata)
