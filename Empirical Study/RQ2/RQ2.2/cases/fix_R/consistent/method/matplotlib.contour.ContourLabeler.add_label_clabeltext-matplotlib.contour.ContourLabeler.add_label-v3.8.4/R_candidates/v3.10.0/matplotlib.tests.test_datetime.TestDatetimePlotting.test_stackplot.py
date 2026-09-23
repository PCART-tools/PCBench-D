    @mpl.style.context("default")
    def test_stackplot(self):
        mpl.rcParams["date.converter"] = 'concise'
        N = 10
        stacked_nums = np.tile(np.arange(1, N), (4, 1))
        dates = np.array([datetime.datetime(2020 + i, 1, 1) for i in range(N - 1)])

        fig, ax = plt.subplots(layout='constrained')
        ax.stackplot(dates, stacked_nums)
