@pytest.mark.flaky(reruns=3)
def test_invisible_Line_rendering():
    """
    GitHub issue #1256 identified a bug in Line.draw method

    Despite visibility attribute set to False, the draw method was not
    returning early enough and some pre-rendering code was executed
    though not necessary.

    Consequence was an excessive draw time for invisible Line instances
    holding a large number of points (Npts> 10**6)
    """
    # Creates big x and y data:
    N = 10**7
    x = np.linspace(0, 1, N)
    y = np.random.normal(size=N)

    # Create a plot figure:
    fig = plt.figure()
    ax = plt.subplot()

    # Create a "big" Line instance:
    l = mlines.Line2D(x, y)
    l.set_visible(False)
    # but don't add it to the Axis instance `ax`

    # [here Interactive panning and zooming is pretty responsive]
    # Time the canvas drawing:
    t_no_line = min(timeit.repeat(fig.canvas.draw, number=1, repeat=3))
    # (gives about 25 ms)

    # Add the big invisible Line:
    ax.add_line(l)

    # [Now interactive panning and zooming is very slow]
    # Time the canvas drawing:
    t_invisible_line = min(timeit.repeat(fig.canvas.draw, number=1, repeat=3))
    # gives about 290 ms for N = 10**7 pts

    slowdown_factor = t_invisible_line / t_no_line
    slowdown_threshold = 2  # trying to avoid false positive failures
    assert slowdown_factor < slowdown_threshold
