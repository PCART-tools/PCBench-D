def test_hist_stacked_step_geometry():
    bins = [0, 1, 2, 3]
    data_1 = [0, 0, 1, 1, 1, 2]
    data_2 = [0, 1, 2]
    _, _, patches = plt.hist([data_1, data_2],
                             bins=bins,
                             stacked=True,
                             histtype='step')

    assert len(patches) == 2

    polygon,  = patches[0]
    xy = [[0, 0], [0, 2], [1, 2], [1, 3], [2, 3], [2, 1], [3, 1], [3, 0]]
    assert_array_equal(polygon.get_xy(), xy)

    polygon,  = patches[1]
    xy = [[0, 2], [0, 3], [1, 3], [1, 4], [2, 4], [2, 2], [3, 2], [3, 1]]
    assert_array_equal(polygon.get_xy(), xy)
