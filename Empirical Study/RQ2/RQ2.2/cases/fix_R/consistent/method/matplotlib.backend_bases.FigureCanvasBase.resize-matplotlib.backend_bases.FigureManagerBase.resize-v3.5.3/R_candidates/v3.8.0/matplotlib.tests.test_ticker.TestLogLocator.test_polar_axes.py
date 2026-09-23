    def test_polar_axes(self):
        """
        Polar axes have a different ticking logic.
        """
        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
        ax.set_yscale('log')
        ax.set_ylim(1, 100)
        assert_array_equal(ax.get_yticks(), [10, 100, 1000])
