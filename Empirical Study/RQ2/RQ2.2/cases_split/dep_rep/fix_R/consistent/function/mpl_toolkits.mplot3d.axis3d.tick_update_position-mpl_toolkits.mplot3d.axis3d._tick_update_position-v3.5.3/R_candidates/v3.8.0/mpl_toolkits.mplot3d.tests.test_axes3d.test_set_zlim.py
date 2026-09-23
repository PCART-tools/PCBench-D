def test_set_zlim():
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    assert ax.get_zlim() == (0, 1)
    ax.set_zlim(zmax=2)
    assert ax.get_zlim() == (0, 2)
    ax.set_zlim(zmin=1)
    assert ax.get_zlim() == (1, 2)

    with pytest.raises(
            TypeError, match="Cannot pass both 'bottom' and 'zmin'"):
        ax.set_zlim(bottom=0, zmin=1)
    with pytest.raises(
            TypeError, match="Cannot pass both 'top' and 'zmax'"):
        ax.set_zlim(top=0, zmax=1)
