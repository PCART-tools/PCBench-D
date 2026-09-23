    @mpl.style.context("default")
    def test_fill_betweenx(self):
        mpl.rcParams["date.converter"] = "concise"
        np.random.seed(19680801)

        x_base_date = datetime.datetime(2023, 1, 1)
        x_dates1 = [x_base_date]
        for i in range(1, 10):
            x_base_date += datetime.timedelta(days=np.random.randint(1, 5))
            x_dates1.append(x_base_date)

        x_dates2 = [x_base_date]
        for i in range(1, 10):
            x_base_date += datetime.timedelta(days=np.random.randint(1, 5))
            x_dates2.append(x_base_date)
        y_values = np.random.rand(10) * 10
        y_values.sort()

        x_values1 = np.random.rand(10) * 10
        x_values2 = x_values1 + np.random.rand(10) * 10
        x_values1.sort()
        x_values2.sort()

        y_base_date = datetime.datetime(2023, 1, 1)
        y_dates = [y_base_date]
        for i in range(1, 10):
            y_base_date += datetime.timedelta(days=np.random.randint(1, 10))
            y_dates.append(y_base_date)

        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, layout="constrained")

        ax1.fill_betweenx(y_values, x_dates1, x_dates2)
        ax2.fill_betweenx(y_dates, x_values1, x_values2)
        ax3.fill_betweenx(y_dates, x_dates1, x_dates2)
