def test_contour_empty_levels():

    x = np.arange(9)
    z = np.random.random((9, 9))

    fig, ax = plt.subplots()
    with pytest.warns(UserWarning) as record:
        ax.contour(x, x, z, levels=[])
    assert len(record) == 1
