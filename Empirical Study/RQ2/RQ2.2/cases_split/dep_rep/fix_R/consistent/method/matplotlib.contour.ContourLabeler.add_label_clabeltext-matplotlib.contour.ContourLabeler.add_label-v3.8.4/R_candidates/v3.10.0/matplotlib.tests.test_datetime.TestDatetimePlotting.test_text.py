    @mpl.style.context("default")
    def test_text(self):
        mpl.rcParams["date.converter"] = 'concise'
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, layout="constrained")

        limit_value = 10
        font_properties = {'family': 'serif', 'size': 12, 'weight': 'bold'}
        test_date = datetime.datetime(2023, 10, 1)

        x_data = np.array(range(1, limit_value))
        y_data = np.array(range(1, limit_value))

        x_dates = np.array(
            [datetime.datetime(2023, 10, n) for n in range(1, limit_value)]
        )
        y_dates = np.array(
            [datetime.datetime(2023, 10, n) for n in range(1, limit_value)]
        )

        ax1.plot(x_dates, y_data)
        ax1.text(test_date, 5, "Inserted Text", **font_properties)

        ax2.plot(x_data, y_dates)
        ax2.text(7, test_date, "Inserted Text", **font_properties)

        ax3.plot(x_dates, y_dates)
        ax3.text(test_date, test_date, "Inserted Text", **font_properties)
