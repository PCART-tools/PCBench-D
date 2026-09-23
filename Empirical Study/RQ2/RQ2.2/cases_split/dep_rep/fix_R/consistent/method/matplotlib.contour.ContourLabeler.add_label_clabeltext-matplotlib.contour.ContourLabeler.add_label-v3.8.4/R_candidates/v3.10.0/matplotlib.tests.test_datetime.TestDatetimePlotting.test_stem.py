    @mpl.style.context("default")
    def test_stem(self):
        mpl.rcParams["date.converter"] = "concise"

        fig, (ax1, ax2, ax3, ax4, ax5, ax6) = plt.subplots(6, 1, layout="constrained")

        limit_value = 10
        above = datetime.datetime(2023, 9, 18)
        below = datetime.datetime(2023, 11, 18)

        x_ranges = np.arange(1, limit_value)
        y_ranges = np.arange(1, limit_value)

        x_dates = np.array(
            [datetime.datetime(2023, 10, n) for n in range(1, limit_value)]
        )
        y_dates = np.array(
            [datetime.datetime(2023, 10, n) for n in range(1, limit_value)]
        )

        ax1.stem(x_dates, y_dates, bottom=above)
        ax2.stem(x_dates, y_ranges, bottom=5)
        ax3.stem(x_ranges, y_dates, bottom=below)

        ax4.stem(x_ranges, y_dates, orientation="horizontal", bottom=above)
        ax5.stem(x_dates, y_ranges, orientation="horizontal", bottom=5)
        ax6.stem(x_ranges, y_dates, orientation="horizontal", bottom=below)
