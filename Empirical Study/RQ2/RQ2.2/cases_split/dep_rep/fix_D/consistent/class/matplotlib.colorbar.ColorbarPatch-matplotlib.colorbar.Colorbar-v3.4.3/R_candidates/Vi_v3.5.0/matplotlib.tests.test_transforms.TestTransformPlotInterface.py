class TestTransformPlotInterface:
    def test_line_extent_axes_coords(self):
        # a simple line in axes coordinates
        ax = plt.axes()
        ax.plot([0.1, 1.2, 0.8], [0.9, 0.5, 0.8], transform=ax.transAxes)
        assert_array_equal(ax.dataLim.get_points(),
                           np.array([[np.inf, np.inf],
                                     [-np.inf, -np.inf]]))

    def test_line_extent_data_coords(self):
        # a simple line in data coordinates
        ax = plt.axes()
        ax.plot([0.1, 1.2, 0.8], [0.9, 0.5, 0.8], transform=ax.transData)
        assert_array_equal(ax.dataLim.get_points(),
                           np.array([[0.1,  0.5], [1.2,  0.9]]))

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

    def test_line_extent_predata_transform_coords(self):
        # a simple line in (offset + data) coordinates
        ax = plt.axes()
        trans = mtransforms.Affine2D().scale(10) + ax.transData
        ax.plot([0.1, 1.2, 0.8], [35, -5, 18], transform=trans)
        assert_array_equal(ax.dataLim.get_points(),
                           np.array([[1., -50.], [12., 350.]]))

    def test_line_extent_compound_coords2(self):
        # a simple line in (offset + data) coordinates in the y component, and
        # in axes coordinates in the x
        ax = plt.axes()
        trans = mtransforms.blended_transform_factory(
            ax.transAxes, mtransforms.Affine2D().scale(10) + ax.transData)
        ax.plot([0.1, 1.2, 0.8], [35, -5, 18], transform=trans)
        assert_array_equal(ax.dataLim.get_points(),
                           np.array([[np.inf, -50.], [-np.inf, 350.]]))

    def test_line_extents_affine(self):
        ax = plt.axes()
        offset = mtransforms.Affine2D().translate(10, 10)
        plt.plot(np.arange(10), transform=offset + ax.transData)
        expected_data_lim = np.array([[0., 0.], [9.,  9.]]) + 10
        assert_array_almost_equal(ax.dataLim.get_points(), expected_data_lim)

    def test_line_extents_non_affine(self):
        ax = plt.axes()
        offset = mtransforms.Affine2D().translate(10, 10)
        na_offset = NonAffineForTest(mtransforms.Affine2D().translate(10, 10))
        plt.plot(np.arange(10), transform=offset + na_offset + ax.transData)
        expected_data_lim = np.array([[0., 0.], [9.,  9.]]) + 20
        assert_array_almost_equal(ax.dataLim.get_points(), expected_data_lim)

    def test_pathc_extents_non_affine(self):
        ax = plt.axes()
        offset = mtransforms.Affine2D().translate(10, 10)
        na_offset = NonAffineForTest(mtransforms.Affine2D().translate(10, 10))
        pth = Path(np.array([[0, 0], [0, 10], [10, 10], [10, 0]]))
        patch = mpatches.PathPatch(pth,
                                   transform=offset + na_offset + ax.transData)
        ax.add_patch(patch)
        expected_data_lim = np.array([[0., 0.], [10.,  10.]]) + 20
        assert_array_almost_equal(ax.dataLim.get_points(), expected_data_lim)

    def test_pathc_extents_affine(self):
        ax = plt.axes()
        offset = mtransforms.Affine2D().translate(10, 10)
        pth = Path(np.array([[0, 0], [0, 10], [10, 10], [10, 0]]))
        patch = mpatches.PathPatch(pth, transform=offset + ax.transData)
        ax.add_patch(patch)
        expected_data_lim = np.array([[0., 0.], [10.,  10.]]) + 10
        assert_array_almost_equal(ax.dataLim.get_points(), expected_data_lim)

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
