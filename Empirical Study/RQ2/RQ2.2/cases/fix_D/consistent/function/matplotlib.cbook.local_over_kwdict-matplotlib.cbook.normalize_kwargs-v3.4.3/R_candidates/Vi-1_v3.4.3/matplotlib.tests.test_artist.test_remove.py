def test_remove():
    fig, ax = plt.subplots()
    im = ax.imshow(np.arange(36).reshape(6, 6))
    ln, = ax.plot(range(5))

    assert fig.stale
    assert ax.stale

    fig.canvas.draw()
    assert not fig.stale
    assert not ax.stale
    assert not ln.stale

    assert im in ax._mouseover_set
    assert ln not in ax._mouseover_set
    assert im.axes is ax

    im.remove()
    ln.remove()

    for art in [im, ln]:
        assert art.axes is None
        assert art.figure is None

    assert im not in ax._mouseover_set
    assert fig.stale
    assert ax.stale
