def test_inverted_cla():
    # GitHub PR #5450. Setting autoscale should reset
    # axes to be non-inverted.
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    # 1. test that a new axis is not inverted per default
    assert not ax.xaxis_inverted()
    assert not ax.yaxis_inverted()
    assert not ax.zaxis_inverted()
    ax.set_xlim(1, 0)
    ax.set_ylim(1, 0)
    ax.set_zlim(1, 0)
    assert ax.xaxis_inverted()
    assert ax.yaxis_inverted()
    assert ax.zaxis_inverted()
    ax.cla()
    assert not ax.xaxis_inverted()
    assert not ax.yaxis_inverted()
    assert not ax.zaxis_inverted()
