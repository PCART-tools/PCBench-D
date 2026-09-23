    def test_line_extents_for_non_affine_transData(self):
        ax = plt.axes(projection='polar')
        # add 10 to the radius of the data
        offset = mtransforms.Affine2D().translate(0, 10)

        plt.plot(np.arange(10), transform=offset + ax.transData)
        # the data lim of a polar plot is stored in coordinates
        # before a transData transformation, hence the data limits
        # are not what is being shown on the actual plot.
        expected_data_lim = np.array([[0., 0.], [9.,  9.]]) + [0, 10]
        assert_array_almost_equal(ax.dataLim.get_points(), expected_data_lim)
