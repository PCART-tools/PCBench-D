    def test_basic(self):
        fig, ax = plt.subplots()
        ax.set_xlim(0, 1.39)
        ax.minorticks_on()
        test_value = np.array([0.05, 0.1, 0.15, 0.25, 0.3, 0.35, 0.45,
                               0.5, 0.55, 0.65, 0.7, 0.75, 0.85, 0.9,
                               0.95, 1, 1.05, 1.1, 1.15, 1.25, 1.3, 1.35])
        assert_almost_equal(ax.xaxis.get_ticklocs(minor=True), test_value)
