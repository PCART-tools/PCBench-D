def test_hist_stacked_step_bottom_geometry():
    bins = [0, 1, 2, 3]
    data_1 = [0, 0, 1, 1, 1, 2]
    data_2 = [0, 1, 2]
    _, _, patches = plt.hist([data_1, data_2],
                             bins=bins,
                             stacked=True,
                             bottom=[1, 2, 1.5],
                             histtype='step')

    assert len(patches) == 2

    polygon,  = patches[0]
    xy = [[0, 1], [0, 3], [1, 3], [1, 5], [2, 5], [2, 2.5], [3, 2.5], [3, 1.5]]
    assert_array_equal(polygon.get_xy(), xy)

    polygon,  = patches[1]
    xy = [[0, 3], [0, 4], [1, 4], [1, 6], [2, 6], [2, 3.5], [3, 3.5], [3, 2.5]]
    assert_array_equal(polygon.get_xy(), xy)
