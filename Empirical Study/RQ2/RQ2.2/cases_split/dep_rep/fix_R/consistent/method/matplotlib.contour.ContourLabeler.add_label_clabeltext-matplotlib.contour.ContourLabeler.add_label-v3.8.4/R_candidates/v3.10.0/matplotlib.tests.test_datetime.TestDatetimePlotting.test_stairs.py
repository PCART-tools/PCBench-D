    @mpl.style.context("default")
    def test_stairs(self):
        mpl.rcParams["date.converter"] = 'concise'

        start_date = datetime.datetime(2023, 12, 1)
        time_delta = datetime.timedelta(days=1)
        baseline_date = datetime.datetime(1980, 1, 1)

        bin_edges = [start_date + i * time_delta for i in range(31)]
        edge_int = np.arange(31)
        np.random.seed(123456)
        values1 = np.random.randint(1, 100, 30)
        values2 = [start_date + datetime.timedelta(days=int(i))
                   for i in np.random.randint(1, 10000, 30)]
        values3 = [start_date + datetime.timedelta(days=int(i))
                   for i in np.random.randint(-10000, 10000, 30)]

        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, constrained_layout=True)
        ax1.stairs(values1, edges=bin_edges)
        ax2.stairs(values2, edges=edge_int, baseline=baseline_date)
        ax3.stairs(values3, edges=bin_edges, baseline=baseline_date)
