    @mpl.style.context("default")
    def test_fill_between(self):
        mpl.rcParams["date.converter"] = "concise"
        np.random.seed(19680801)

        y_base_date = datetime.datetime(2023, 1, 1)
        y_dates1 = [y_base_date]
        for i in range(1, 10):
            y_base_date += datetime.timedelta(days=np.random.randint(1, 5))
            y_dates1.append(y_base_date)

        y_dates2 = [y_base_date]
        for i in range(1, 10):
            y_base_date += datetime.timedelta(days=np.random.randint(1, 5))
            y_dates2.append(y_base_date)
        x_values = np.random.rand(10) * 10
        x_values.sort()

        y_values1 = np.random.rand(10) * 10
        y_values2 = y_values1 + np.random.rand(10) * 10
        y_values1.sort()
        y_values2.sort()

        x_base_date = datetime.datetime(2023, 1, 1)
        x_dates = [x_base_date]
        for i in range(1, 10):
            x_base_date += datetime.timedelta(days=np.random.randint(1, 10))
            x_dates.append(x_base_date)

        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, layout="constrained")

        ax1.fill_between(x_values, y_dates1, y_dates2)
        ax2.fill_between(x_dates, y_values1, y_values2)
        ax3.fill_between(x_dates, y_dates1, y_dates2)
