def test_multiplot_autoscale():
    fig = plt.figure()
    ax1, ax2 = fig.subplots(2, 1, sharex='all')
    ax1.scatter([1, 2, 3, 4], [2, 3, 2, 3])
    ax2.axhspan(-5, 5)
    xlim = ax1.get_xlim()
    assert np.allclose(xlim, [0.5, 4.5])
