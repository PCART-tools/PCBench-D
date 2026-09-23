def test_margins():
    # test all ways margins can be called
    data = [1, 10]
    xmin = 0.0
    xmax = len(data) - 1.0
    ymin = min(data)
    ymax = max(data)

    fig1, ax1 = plt.subplots(1, 1)
    ax1.plot(data)
    ax1.margins(1)
    assert ax1.margins() == (1, 1)
    assert ax1.get_xlim() == (xmin - (xmax - xmin) * 1,
                              xmax + (xmax - xmin) * 1)
    assert ax1.get_ylim() == (ymin - (ymax - ymin) * 1,
                              ymax + (ymax - ymin) * 1)

    fig2, ax2 = plt.subplots(1, 1)
    ax2.plot(data)
    ax2.margins(0.5, 2)
    assert ax2.margins() == (0.5, 2)
    assert ax2.get_xlim() == (xmin - (xmax - xmin) * 0.5,
                              xmax + (xmax - xmin) * 0.5)
    assert ax2.get_ylim() == (ymin - (ymax - ymin) * 2,
                              ymax + (ymax - ymin) * 2)

    fig3, ax3 = plt.subplots(1, 1)
    ax3.plot(data)
    ax3.margins(x=-0.2, y=0.5)
    assert ax3.margins() == (-0.2, 0.5)
    assert ax3.get_xlim() == (xmin - (xmax - xmin) * -0.2,
                              xmax + (xmax - xmin) * -0.2)
    assert ax3.get_ylim() == (ymin - (ymax - ymin) * 0.5,
                              ymax + (ymax - ymin) * 0.5)
