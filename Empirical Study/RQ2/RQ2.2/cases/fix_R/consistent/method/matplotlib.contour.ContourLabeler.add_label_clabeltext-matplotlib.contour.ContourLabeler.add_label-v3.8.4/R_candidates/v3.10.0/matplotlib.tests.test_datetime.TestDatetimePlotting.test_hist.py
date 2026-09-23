    @mpl.style.context("default")
    def test_hist(self):
        mpl.rcParams["date.converter"] = 'concise'

        start_date = datetime.datetime(2023, 10, 1)
        time_delta = datetime.timedelta(days=1)

        values1 = np.random.randint(1, 10, 30)
        values2 = np.random.randint(1, 10, 30)
        values3 = np.random.randint(1, 10, 30)

        bin_edges = [start_date + i * time_delta for i in range(31)]

        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, constrained_layout=True)
        ax1.hist(
            [start_date + i * time_delta for i in range(30)],
            bins=10,
            weights=values1
        )
        ax2.hist(
            [start_date + i * time_delta for i in range(30)],
            bins=10,
            weights=values2
        )
        ax3.hist(
            [start_date + i * time_delta for i in range(30)],
            bins=10,
            weights=values3
        )

        fig, (ax4, ax5, ax6) = plt.subplots(3, 1, constrained_layout=True)
        ax4.hist(
            [start_date + i * time_delta for i in range(30)],
            bins=bin_edges,
            weights=values1
        )
        ax5.hist(
            [start_date + i * time_delta for i in range(30)],
            bins=bin_edges,
            weights=values2
        )
        ax6.hist(
            [start_date + i * time_delta for i in range(30)],
            bins=bin_edges,
            weights=values3
        )
