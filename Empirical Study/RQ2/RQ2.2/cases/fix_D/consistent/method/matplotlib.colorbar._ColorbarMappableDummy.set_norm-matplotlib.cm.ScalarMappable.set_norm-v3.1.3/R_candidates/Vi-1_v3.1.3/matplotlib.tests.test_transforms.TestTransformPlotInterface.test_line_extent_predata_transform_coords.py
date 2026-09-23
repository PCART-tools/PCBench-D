    def test_line_extent_predata_transform_coords(self):
        # a simple line in (offset + data) coordinates
        ax = plt.axes()
        trans = mtransforms.Affine2D().scale(10) + ax.transData
        ax.plot([0.1, 1.2, 0.8], [35, -5, 18], transform=trans)
        assert_array_equal(ax.dataLim.get_points(),
                           np.array([[1., -50.], [12., 350.]]))
        plt.close()
