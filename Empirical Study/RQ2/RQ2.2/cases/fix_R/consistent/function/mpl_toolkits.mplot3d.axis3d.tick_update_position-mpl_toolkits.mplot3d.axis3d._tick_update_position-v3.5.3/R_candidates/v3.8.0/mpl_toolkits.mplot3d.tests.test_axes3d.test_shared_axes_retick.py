def test_shared_axes_retick():
    fig = plt.figure()
    ax1 = fig.add_subplot(211, projection="3d")
    ax2 = fig.add_subplot(212, projection="3d", sharez=ax1)
    ax1.plot([0, 1], [0, 1], [0, 2])
    ax2.plot([0, 1], [0, 1], [0, 2])
    ax1.set_zticks([-0.5, 0, 2, 2.5])
    # check that setting ticks on a shared axis is synchronized
    assert ax1.get_zlim() == (-0.5, 2.5)
    assert ax2.get_zlim() == (-0.5, 2.5)
