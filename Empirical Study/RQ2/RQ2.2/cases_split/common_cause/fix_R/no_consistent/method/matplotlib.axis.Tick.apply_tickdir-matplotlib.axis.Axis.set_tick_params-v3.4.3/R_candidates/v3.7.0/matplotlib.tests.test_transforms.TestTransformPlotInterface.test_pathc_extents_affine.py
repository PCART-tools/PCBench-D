    def test_pathc_extents_affine(self):
        ax = plt.axes()
        offset = mtransforms.Affine2D().translate(10, 10)
        pth = Path([[0, 0], [0, 10], [10, 10], [10, 0]])
        patch = mpatches.PathPatch(pth, transform=offset + ax.transData)
        ax.add_patch(patch)
        expected_data_lim = np.array([[0., 0.], [10.,  10.]]) + 10
        assert_array_almost_equal(ax.dataLim.get_points(), expected_data_lim)
