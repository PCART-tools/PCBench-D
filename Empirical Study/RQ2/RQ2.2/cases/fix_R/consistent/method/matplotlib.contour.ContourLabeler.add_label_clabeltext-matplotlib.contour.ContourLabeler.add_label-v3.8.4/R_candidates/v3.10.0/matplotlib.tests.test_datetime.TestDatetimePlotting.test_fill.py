    @mpl.style.context("default")
    def test_fill(self):
        mpl.rcParams["date.converter"] = "concise"
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, layout="constrained")

        np.random.seed(19680801)

        x_base_date = datetime.datetime(2023, 1, 1)
        x_dates = [x_base_date]
        for _ in range(1, 5):
            x_base_date += datetime.timedelta(days=np.random.randint(1, 5))
            x_dates.append(x_base_date)

        y_base_date = datetime.datetime(2023, 1, 1)
        y_dates = [y_base_date]
        for _ in range(1, 5):
            y_base_date += datetime.timedelta(days=np.random.randint(1, 5))
            y_dates.append(y_base_date)

        x_values = np.random.rand(5) * 5
        y_values = np.random.rand(5) * 5 - 2

        ax1.fill(x_dates, y_values)
        ax2.fill(x_values, y_dates)
        ax3.fill(x_values, y_values)
        ax4.fill(x_dates, y_dates)
