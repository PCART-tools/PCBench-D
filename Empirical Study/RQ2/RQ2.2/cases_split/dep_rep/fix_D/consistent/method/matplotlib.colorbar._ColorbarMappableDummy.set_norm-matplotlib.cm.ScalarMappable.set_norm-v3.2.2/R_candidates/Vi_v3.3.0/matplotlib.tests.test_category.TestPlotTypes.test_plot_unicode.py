    @pytest.mark.parametrize("plotter", PLOT_LIST, ids=PLOT_IDS)
    def test_plot_unicode(self, ax, plotter):
        words = ['Здравствуйте', 'привет']
        plotter(ax, words, [0, 1])
        axis_test(ax.xaxis, words)
