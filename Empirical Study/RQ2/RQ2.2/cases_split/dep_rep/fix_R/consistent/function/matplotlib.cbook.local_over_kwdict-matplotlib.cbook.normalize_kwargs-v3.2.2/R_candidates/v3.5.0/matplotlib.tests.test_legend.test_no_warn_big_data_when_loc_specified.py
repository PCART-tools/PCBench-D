def test_no_warn_big_data_when_loc_specified():
    fig, ax = plt.subplots()
    fig.canvas.draw()
    for idx in range(1000):
        ax.plot(np.arange(5000), label=idx)
    legend = ax.legend('best')
    fig.draw_artist(legend)  # Check that no warning is emitted.
