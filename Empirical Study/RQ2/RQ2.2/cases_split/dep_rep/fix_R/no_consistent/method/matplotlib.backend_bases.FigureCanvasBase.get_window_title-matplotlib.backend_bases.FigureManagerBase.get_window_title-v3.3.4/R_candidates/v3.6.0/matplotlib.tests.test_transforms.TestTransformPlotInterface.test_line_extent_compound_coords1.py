    def test_line_extent_compound_coords1(self):
        # a simple line in data coordinates in the y component, and in axes
        # coordinates in the x
        ax = plt.axes()
        trans = mtransforms.blended_transform_factory(ax.transAxes,
                                                      ax.transData)
        ax.plot([0.1, 1.2, 0.8], [35, -5, 18], transform=trans)
        assert_array_equal(ax.dataLim.get_points(),
                           np.array([[np.inf, -5.],
                                     [-np.inf, 35.]]))
