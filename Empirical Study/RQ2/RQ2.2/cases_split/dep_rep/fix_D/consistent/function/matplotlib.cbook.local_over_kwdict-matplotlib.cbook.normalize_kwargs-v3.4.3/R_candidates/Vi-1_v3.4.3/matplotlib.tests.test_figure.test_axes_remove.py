def test_axes_remove():
    fig, axs = plt.subplots(2, 2)
    axs[-1, -1].remove()
    for ax in axs.ravel()[:-1]:
        assert ax in fig.axes
    assert axs[-1, -1] not in fig.axes
    assert len(fig.axes) == 3
