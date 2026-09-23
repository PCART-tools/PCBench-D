    def test_line_extents_affine(self):
        ax = plt.axes()
        offset = mtransforms.Affine2D().translate(10, 10)
        plt.plot(np.arange(10), transform=offset + ax.transData)
        expected_data_lim = np.array([[0., 0.], [9.,  9.]]) + 10
        assert_array_almost_equal(ax.dataLim.get_points(), expected_data_lim)
