    @mpl.style.context("default")
    def test_plot_date(self):
        mpl.rcParams["date.converter"] = "concise"
        range_threshold = 10
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, layout="constrained")

        x_dates = np.array(
            [datetime.datetime(2023, 10, delta) for delta in range(1, range_threshold)]
        )
        y_dates = np.array(
            [datetime.datetime(2023, 10, delta) for delta in range(1, range_threshold)]
        )
        x_ranges = np.array(range(1, range_threshold))
        y_ranges = np.array(range(1, range_threshold))

        with pytest.warns(mpl.MatplotlibDeprecationWarning):
            ax1.plot_date(x_dates, y_dates)
            ax2.plot_date(x_dates, y_ranges)
            ax3.plot_date(x_ranges, y_dates)
