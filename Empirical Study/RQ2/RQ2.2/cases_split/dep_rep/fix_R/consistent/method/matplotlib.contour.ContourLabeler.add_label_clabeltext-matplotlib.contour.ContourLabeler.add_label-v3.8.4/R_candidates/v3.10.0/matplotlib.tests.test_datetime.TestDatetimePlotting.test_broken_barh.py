    @mpl.style.context("default")
    def test_broken_barh(self):
        # Horizontal bar plot with gaps
        mpl.rcParams["date.converter"] = 'concise'
        fig, ax = plt.subplots()

        ax.broken_barh([(datetime.datetime(2023, 1, 4), datetime.timedelta(days=2)),
                        (datetime.datetime(2023, 1, 8), datetime.timedelta(days=3))],
                        (10, 9), facecolors='tab:blue')
        ax.broken_barh([(datetime.datetime(2023, 1, 2), datetime.timedelta(days=1)),
                         (datetime.datetime(2023, 1, 4), datetime.timedelta(days=4))],
                         (20, 9), facecolors=('tab:red'))
