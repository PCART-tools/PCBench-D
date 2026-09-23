    @mpl.style.context("default")
    def test_axvline(self):
        mpl.rcParams["date.converter"] = 'concise'
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, layout='constrained')
        ax1.set_xlim(left=datetime.datetime(2020, 4, 1),
                     right=datetime.datetime(2020, 8, 1))
        ax2.set_xlim(left=np.datetime64('2005-01-01'),
                     right=np.datetime64('2005-04-01'))
        ax3.set_xlim(left=datetime.datetime(2023, 9, 1),
                     right=datetime.datetime(2023, 11, 1))
        ax1.axvline(x=datetime.datetime(2020, 6, 3), ymin=0.5, ymax=0.7)
        ax2.axvline(np.datetime64('2005-02-25T03:30'), ymin=0.1, ymax=0.9)
        ax3.axvline(x=datetime.datetime(2023, 10, 24), ymin=0.4, ymax=0.7)
