    @mpl.style.context("default")
    def test_errorbar(self):
        mpl.rcParams["date.converter"] = "concise"
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, layout="constrained")
        limit = 7
        start_date = datetime.datetime(2023, 1, 1)

        x_dates = np.array([datetime.datetime(2023, 10, d) for d in range(1, limit)])
        y_dates = np.array([datetime.datetime(2023, 10, d) for d in range(1, limit)])
        x_date_error = datetime.timedelta(days=1)
        y_date_error = datetime.timedelta(days=1)

        x_values = list(range(1, limit))
        y_values = list(range(1, limit))
        x_value_error = 0.5
        y_value_error = 0.5

        ax1.errorbar(x_dates, y_values,
                     yerr=y_value_error,
                     capsize=10,
                     barsabove=True,
                     label='Data')
        ax2.errorbar(x_values, y_dates,
                     xerr=x_value_error, yerr=y_date_error,
                     errorevery=(1, 2),
                     fmt='-o', label='Data')
        ax3.errorbar(x_dates, y_dates,
                     xerr=x_date_error, yerr=y_date_error,
                     lolims=True, xlolims=True,
                     label='Data')
        ax4.errorbar(x_dates, y_values,
                     xerr=x_date_error, yerr=y_value_error,
                     uplims=True, xuplims=True,
                     label='Data')
