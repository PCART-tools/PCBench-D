class TestPlotTypes:
    @pytest.mark.parametrize("plotter", PLOT_LIST, ids=PLOT_IDS)
    def test_plot_unicode(self, plotter):
        ax = plt.figure().subplots()
        words = ['Здравствуйте', 'привет']
        plotter(ax, words, [0, 1])
        axis_test(ax.xaxis, words)

    @pytest.fixture
    def test_data(self):
        self.x = ["hello", "happy", "world"]
        self.xy = [2, 6, 3]
        self.y = ["Python", "is", "fun"]
        self.yx = [3, 4, 5]

    @pytest.mark.usefixtures("test_data")
    @pytest.mark.parametrize("plotter", PLOT_LIST, ids=PLOT_IDS)
    def test_plot_xaxis(self, test_data, plotter):
        ax = plt.figure().subplots()
        plotter(ax, self.x, self.xy)
        axis_test(ax.xaxis, self.x)

    @pytest.mark.usefixtures("test_data")
    @pytest.mark.parametrize("plotter", PLOT_LIST, ids=PLOT_IDS)
    def test_plot_yaxis(self, test_data, plotter):
        ax = plt.figure().subplots()
        plotter(ax, self.yx, self.y)
        axis_test(ax.yaxis, self.y)

    @pytest.mark.usefixtures("test_data")
    @pytest.mark.parametrize("plotter", PLOT_LIST, ids=PLOT_IDS)
    def test_plot_xyaxis(self, test_data, plotter):
        ax = plt.figure().subplots()
        plotter(ax, self.x, self.y)
        axis_test(ax.xaxis, self.x)
        axis_test(ax.yaxis, self.y)

    @pytest.mark.parametrize("plotter", PLOT_LIST, ids=PLOT_IDS)
    def test_update_plot(self, plotter):
        ax = plt.figure().subplots()
        plotter(ax, ['a', 'b'], ['e', 'g'])
        plotter(ax, ['a', 'b', 'd'], ['f', 'a', 'b'])
        plotter(ax, ['b', 'c', 'd'], ['g', 'e', 'd'])
        axis_test(ax.xaxis, ['a', 'b', 'd', 'c'])
        axis_test(ax.yaxis, ['e', 'g', 'f', 'a', 'b', 'd'])

    failing_test_cases = [("mixed", ['A', 3.14]),
                          ("number integer", ['1', 1]),
                          ("string integer", ['42', 42]),
                          ("missing", ['12', np.nan])]

    fids, fvalues = zip(*failing_test_cases)

    plotters = [Axes.scatter, Axes.bar,
                pytest.param(Axes.plot, marks=pytest.mark.xfail)]

    @pytest.mark.parametrize("plotter", plotters)
    @pytest.mark.parametrize("xdata", fvalues, ids=fids)
    def test_mixed_type_exception(self, plotter, xdata):
        ax = plt.figure().subplots()
        with pytest.raises(TypeError):
            plotter(ax, xdata, [1, 2])

    @pytest.mark.parametrize("plotter", plotters)
    @pytest.mark.parametrize("xdata", fvalues, ids=fids)
    def test_mixed_type_update_exception(self, plotter, xdata):
        ax = plt.figure().subplots()
        with pytest.raises(TypeError):
            plotter(ax, [0, 3], [1, 3])
            plotter(ax, xdata, [1, 2])
