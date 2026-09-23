    @mpl.style.context("default")
    def test_axhspan(self):
        mpl.rcParams["date.converter"] = 'concise'

        start_date = datetime.datetime(2023, 1, 1)
        dates = [start_date + datetime.timedelta(days=i) for i in range(31)]
        numbers = list(range(1, 32))

        fig, (ax1, ax2, ax3) = plt.subplots(3, 1,
                                            constrained_layout=True,
                                            figsize=(10, 12))

        ax1.plot(dates, numbers, marker='o', color='blue')
        for i in range(0, 31, 2):
            ax1.axhspan(ymin=i+1, ymax=i+2, facecolor='green', alpha=0.5)
        ax1.set_title('Datetime vs. Number')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Number')

        ax2.plot(numbers, dates, marker='o', color='blue')
        for i in range(0, 31, 2):
            ymin = start_date + datetime.timedelta(days=i)
            ymax = ymin + datetime.timedelta(days=1)
            ax2.axhspan(ymin=ymin, ymax=ymax, facecolor='green', alpha=0.5)
        ax2.set_title('Number vs. Datetime')
        ax2.set_xlabel('Number')
        ax2.set_ylabel('Date')

        ax3.plot(dates, dates, marker='o', color='blue')
        for i in range(0, 31, 2):
            ymin = start_date + datetime.timedelta(days=i)
            ymax = ymin + datetime.timedelta(days=1)
            ax3.axhspan(ymin=ymin, ymax=ymax, facecolor='green', alpha=0.5)
        ax3.set_title('Datetime vs. Datetime')
        ax3.set_xlabel('Date')
        ax3.set_ylabel('Date')
