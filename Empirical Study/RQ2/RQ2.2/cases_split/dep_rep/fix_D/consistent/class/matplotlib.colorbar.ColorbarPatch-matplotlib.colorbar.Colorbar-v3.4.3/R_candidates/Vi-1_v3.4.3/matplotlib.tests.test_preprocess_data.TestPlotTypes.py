class TestPlotTypes:

    plotters = [Axes.scatter, Axes.bar, Axes.plot]

    @pytest.mark.parametrize('plotter', plotters)
    @check_figures_equal(extensions=['png'])
    def test_dict_unpack(self, plotter, fig_test, fig_ref):
        x = [1, 2, 3]
        y = [4, 5, 6]
        ddict = dict(zip(x, y))

        plotter(fig_test.subplots(),
                ddict.keys(), ddict.values())
        plotter(fig_ref.subplots(), x, y)

    @pytest.mark.parametrize('plotter', plotters)
    @check_figures_equal(extensions=['png'])
    def test_data_kwarg(self, plotter, fig_test, fig_ref):
        x = [1, 2, 3]
        y = [4, 5, 6]

        plotter(fig_test.subplots(), 'xval', 'yval',
                data={'xval': x, 'yval': y})
        plotter(fig_ref.subplots(), x, y)
