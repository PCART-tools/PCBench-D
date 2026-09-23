    @mpl.style.context("default")
    def test_barbs(self):
        plt.rcParams["date.converter"] = 'concise'

        start_date = datetime.datetime(2022, 2, 8, 22)
        dates = [start_date + datetime.timedelta(hours=i) for i in range(12)]

        numbers = np.sin(np.linspace(0, 2 * np.pi, 12))

        u = np.ones(12) * 10
        v = np.arange(0, 120, 10)

        fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))

        axes[0].barbs(dates, numbers, u, v, length=7)
        axes[0].set_title('Datetime vs. Numeric Data')
        axes[0].set_xlabel('Datetime')
        axes[0].set_ylabel('Numeric Data')

        axes[1].barbs(numbers, dates, u, v, length=7)
        axes[1].set_title('Numeric vs. Datetime Data')
        axes[1].set_xlabel('Numeric Data')
        axes[1].set_ylabel('Datetime')
