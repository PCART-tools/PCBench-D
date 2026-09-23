    @mpl.style.context("default")
    def test_matshow(self):
        a = np.diag(range(5))
        dt_start = datetime.datetime(1980, 4, 15)
        dt_end = datetime.datetime(2020, 11, 11)
        extent = (dt_start, dt_end, dt_start, dt_end)
        fig, ax = plt.subplots()
        ax.matshow(a, extent=extent)
        for label in ax.get_xticklabels():
            label.set_rotation(90)
