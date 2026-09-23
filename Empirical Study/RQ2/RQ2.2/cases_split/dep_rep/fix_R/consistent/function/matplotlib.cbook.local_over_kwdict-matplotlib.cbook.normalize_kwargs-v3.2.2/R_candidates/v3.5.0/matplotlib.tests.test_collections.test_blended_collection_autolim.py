def test_blended_collection_autolim():
    a = [1, 2, 4]
    height = .2

    xy_pairs = np.column_stack([np.repeat(a, 2), np.tile([0, height], len(a))])
    line_segs = xy_pairs.reshape([len(a), 2, 2])

    f, ax = plt.subplots()
    trans = mtransforms.blended_transform_factory(ax.transData, ax.transAxes)
    ax.add_collection(LineCollection(line_segs, transform=trans))
    ax.autoscale_view(scalex=True, scaley=False)
    np.testing.assert_allclose(ax.get_xlim(), [1., 4.])
