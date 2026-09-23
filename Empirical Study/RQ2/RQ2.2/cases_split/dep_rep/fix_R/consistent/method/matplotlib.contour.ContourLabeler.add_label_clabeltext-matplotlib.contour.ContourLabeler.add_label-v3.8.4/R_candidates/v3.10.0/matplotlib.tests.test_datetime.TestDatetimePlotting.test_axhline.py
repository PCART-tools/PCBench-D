    @mpl.style.context("default")
    def test_axhline(self):
        mpl.rcParams["date.converter"] = 'concise'
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, layout='constrained')
        ax1.set_ylim(bottom=datetime.datetime(2020, 4, 1),
                     top=datetime.datetime(2020, 8, 1))
        ax2.set_ylim(bottom=np.datetime64('2005-01-01'),
                     top=np.datetime64('2005-04-01'))
        ax3.set_ylim(bottom=datetime.datetime(2023, 9, 1),
                     top=datetime.datetime(2023, 11, 1))
        ax1.axhline(y=datetime.datetime(2020, 6, 3), xmin=0.5, xmax=0.7)
        ax2.axhline(np.datetime64('2005-02-25T03:30'), xmin=0.1, xmax=0.9)
        ax3.axhline(y=datetime.datetime(2023, 10, 24), xmin=0.4, xmax=0.7)
