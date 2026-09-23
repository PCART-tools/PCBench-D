    @mpl.style.context("default")
    def test_imshow(self):
        fig, ax = plt.subplots()
        a = np.diag(range(5))
        dt_start = datetime.datetime(2010, 11, 1)
        dt_end = datetime.datetime(2010, 11, 11)
        extent = (dt_start, dt_end, dt_start, dt_end)
        ax.imshow(a, extent=extent)
        ax.tick_params(axis="x", labelrotation=90)
