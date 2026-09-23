    @mpl.style.context("default")
    def test_contour(self):
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

        X_dates, Y_dates = np.meshgrid(x_dates, y_dates)
        X_ranges, Y_ranges = np.meshgrid(x_ranges, y_ranges)

        Z_ranges = np.cos(X_ranges / 4) + np.sin(Y_ranges / 4)

        ax1.contour(X_dates, Y_dates, Z_ranges)
        ax2.contour(X_dates, Y_ranges, Z_ranges)
        ax3.contour(X_ranges, Y_dates, Z_ranges)
