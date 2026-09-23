    @mpl.style.context("default")
    def test_eventplot(self):
        mpl.rcParams["date.converter"] = "concise"

        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, layout="constrained")

        x_dates1 = np.array([datetime.datetime(2020, 6, 30),
                             datetime.datetime(2020, 7, 22),
                             datetime.datetime(2020, 8, 3),
                             datetime.datetime(2020, 9, 14),],
                            dtype=np.datetime64,
                            )

        ax1.eventplot(x_dates1)

        np.random.seed(19680801)

        start_date = datetime.datetime(2020, 7, 1)
        end_date = datetime.datetime(2020, 10, 15)
        date_range = end_date - start_date

        dates1 = start_date + np.random.rand(30) * date_range
        dates2 = start_date + np.random.rand(10) * date_range
        dates3 = start_date + np.random.rand(50) * date_range

        colors1 = ['C1', 'C2', 'C3']
        lineoffsets1 = np.array([1, 6, 8])
        linelengths1 = [5, 2, 3]

        ax2.eventplot([dates1, dates2, dates3],
                      colors=colors1,
                      lineoffsets=lineoffsets1,
                      linelengths=linelengths1)

        lineoffsets2 = np.array([
            datetime.datetime(2020, 7, 1),
            datetime.datetime(2020, 7, 15),
            datetime.datetime(2020, 8, 1)
        ], dtype=np.datetime64)

        ax3.eventplot([dates1, dates2, dates3],
                      colors=colors1,
                      lineoffsets=lineoffsets2,
                      linelengths=linelengths1)
