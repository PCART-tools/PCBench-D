    @mpl.style.context("default")
    def test_hlines(self):
        mpl.rcParams["date.converter"] = 'concise'
        fig, axs = plt.subplots(2, 4, layout='constrained')
        dateStrs = ['2023-03-08',
                    '2023-04-09',
                    '2023-05-13',
                    '2023-07-28',
                    '2023-12-24']
        dates = [datetime.datetime(2023, m*2, 10) for m in range(1, 6)]
        date_start = [datetime.datetime(2023, 6, d) for d in range(5, 30, 5)]
        date_end = [datetime.datetime(2023, 7, d) for d in range(5, 30, 5)]
        npDates = [np.datetime64(s) for s in dateStrs]
        axs[0, 0].hlines(y=dates,
                         xmin=[0.1, 0.2, 0.3, 0.4, 0.5],
                         xmax=[0.5, 0.6, 0.7, 0.8, 0.9])
        axs[0, 1].hlines(dates,
                         xmin=datetime.datetime(2020, 5, 10),
                         xmax=datetime.datetime(2020, 5, 31))
        axs[0, 2].hlines(dates,
                         xmin=date_start,
                         xmax=date_end)
        axs[0, 3].hlines(dates,
                         xmin=0.45,
                         xmax=0.65)
        axs[1, 0].hlines(y=npDates,
                         xmin=[0.5, 0.6, 0.7, 0.8, 0.9],
                         xmax=[0.1, 0.2, 0.3, 0.4, 0.5])
        axs[1, 2].hlines(y=npDates,
                         xmin=date_start,
                         xmax=date_end)
        axs[1, 1].hlines(npDates,
                         xmin=datetime.datetime(2020, 5, 10),
                         xmax=datetime.datetime(2020, 5, 31))
        axs[1, 3].hlines(npDates,
                         xmin=0.45,
                         xmax=0.65)
