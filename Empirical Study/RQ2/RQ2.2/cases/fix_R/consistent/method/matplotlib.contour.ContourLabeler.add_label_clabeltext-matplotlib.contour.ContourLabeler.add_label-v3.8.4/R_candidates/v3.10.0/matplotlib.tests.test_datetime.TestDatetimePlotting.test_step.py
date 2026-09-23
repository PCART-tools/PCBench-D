    @mpl.style.context("default")
    def test_step(self):
        mpl.rcParams["date.converter"] = "concise"
        N = 6
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, layout='constrained')
        x = np.array([datetime.datetime(2023, 9, n) for n in range(1, N)])
        ax1.step(x, range(1, N))
        ax2.step(range(1, N), x)
        ax3.step(x, x)
