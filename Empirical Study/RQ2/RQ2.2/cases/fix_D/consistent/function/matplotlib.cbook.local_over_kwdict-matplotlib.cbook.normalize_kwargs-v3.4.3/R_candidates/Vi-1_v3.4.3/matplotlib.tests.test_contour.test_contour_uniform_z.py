def test_contour_uniform_z():

    x = np.arange(9)
    z = np.ones((9, 9))

    fig, ax = plt.subplots()
    with pytest.warns(UserWarning) as record:
        ax.contour(x, x, z)
    assert len(record) == 1
