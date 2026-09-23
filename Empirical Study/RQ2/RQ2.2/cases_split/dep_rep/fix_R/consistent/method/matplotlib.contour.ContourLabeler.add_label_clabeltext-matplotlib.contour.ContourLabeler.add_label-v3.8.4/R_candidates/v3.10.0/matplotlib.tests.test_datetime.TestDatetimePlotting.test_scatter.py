    @mpl.style.context("default")
    def test_scatter(self):
        mpl.rcParams["date.converter"] = 'concise'
        base = datetime.datetime(2005, 2, 1)
        dates = [base + datetime.timedelta(hours=(2 * i)) for i in range(10)]
        N = len(dates)
        np.random.seed(19680801)
        y = np.cumsum(np.random.randn(N))
        fig, axs = plt.subplots(3, 1, layout='constrained', figsize=(6, 6))
        # datetime array on x axis
        axs[0].scatter(dates, y)
        for label in axs[0].get_xticklabels():
            label.set_rotation(40)
            label.set_horizontalalignment('right')
        # datetime on y axis
        axs[1].scatter(y, dates)
        # datetime on both x, y axes
        axs[2].scatter(dates, dates)
        for label in axs[2].get_xticklabels():
            label.set_rotation(40)
            label.set_horizontalalignment('right')
