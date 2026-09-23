def test_subfigure_legend():
    # Test that legend can be added to subfigure (#20723)
    subfig = plt.figure().subfigures()
    ax = subfig.subplots()
    ax.plot([0, 1], [0, 1], label="line")
    leg = subfig.legend()
    assert leg.figure is subfig
