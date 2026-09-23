    def test_line_extent_axes_coords(self):
        # a simple line in axes coordinates
        ax = plt.axes()
        ax.plot([0.1, 1.2, 0.8], [0.9, 0.5, 0.8], transform=ax.transAxes)
        assert_array_equal(ax.dataLim.get_points(),
                           np.array([[np.inf, np.inf],
                                     [-np.inf, -np.inf]]))
