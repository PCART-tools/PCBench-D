class TestPlotNumlike:
    numlike_cases = [('string list', ['1', '11', '3']),
                     ('string ndarray', np.array(['1', '11', '3'])),
                     ('bytes list', [b'1', b'11', b'3']),
                     ('bytes ndarray', np.array([b'1', b'11', b'3']))]
    numlike_ids, numlike_data = zip(*numlike_cases)

    @pytest.mark.parametrize("plotter", PLOT_LIST, ids=PLOT_IDS)
    @pytest.mark.parametrize("ndata", numlike_data, ids=numlike_ids)
    def test_plot_numlike(self, ax, plotter, ndata):
        counts = np.array([4, 6, 5])
        plotter(ax, ndata, counts)
        axis_test(ax.xaxis, ndata)
