def test_hist_stepfilled_geometry():
    bins = [0, 1, 2, 3]
    data = [0, 0, 1, 1, 1, 2]
    _, _, (polygon, ) = plt.hist(data,
                                 bins=bins,
                                 histtype='stepfilled')
    xy = [[0, 0], [0, 2], [1, 2], [1, 3], [2, 3], [2, 1], [3, 1],
          [3, 0], [2, 0], [2, 0], [1, 0], [1, 0], [0, 0]]
    assert_array_equal(polygon.get_xy(), xy)
