    @mpl.style.context("default")
    def test_bar(self):
        mpl.rcParams["date.converter"] = "concise"

        fig, (ax1, ax2) = plt.subplots(2, 1, layout="constrained")

        x_dates = np.array(
            [
                datetime.datetime(2020, 6, 30),
                datetime.datetime(2020, 7, 22),
                datetime.datetime(2020, 8, 3),
                datetime.datetime(2020, 9, 14),
            ],
            dtype=np.datetime64,
        )
        x_ranges = [8800, 2600, 8500, 7400]

        x = np.datetime64(datetime.datetime(2020, 6, 1))
        ax1.bar(x_dates, x_ranges, width=np.timedelta64(4, "D"))
        ax2.bar(np.arange(4), x_dates - x, bottom=x)
