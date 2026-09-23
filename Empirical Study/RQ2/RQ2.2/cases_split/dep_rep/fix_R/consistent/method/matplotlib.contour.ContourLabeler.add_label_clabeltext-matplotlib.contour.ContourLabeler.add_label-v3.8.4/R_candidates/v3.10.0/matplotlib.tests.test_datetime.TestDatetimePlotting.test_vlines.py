    @mpl.style.context("default")
    def test_vlines(self):
        mpl.rcParams["date.converter"] = 'concise'
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, layout='constrained')
        ax1.set_xlim(left=datetime.datetime(2023, 1, 1),
                     right=datetime.datetime(2023, 6, 30))
        ax1.vlines(x=[datetime.datetime(2023, 2, 10),
                      datetime.datetime(2023, 5, 18),
                      datetime.datetime(2023, 6, 6)],
                   ymin=[0, 0.25, 0.5],
                   ymax=[0.25, 0.5, 0.75])
        ax2.set_xlim(left=0,
                     right=0.5)
        ax2.vlines(x=[0.3, 0.35],
                   ymin=[np.datetime64('2023-03-20'), np.datetime64('2023-03-31')],
                   ymax=[np.datetime64('2023-05-01'), np.datetime64('2023-05-16')])
        ax3.set_xlim(left=datetime.datetime(2023, 7, 1),
                     right=datetime.datetime(2023, 12, 31))
        ax3.vlines(x=[datetime.datetime(2023, 9, 1), datetime.datetime(2023, 12, 10)],
                   ymin=datetime.datetime(2023, 1, 15),
                   ymax=datetime.datetime(2023, 1, 30))
