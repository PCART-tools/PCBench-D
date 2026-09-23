def test_warn_big_data_best_loc():
    fig, ax = plt.subplots()
    fig.canvas.draw()  # So that we can call draw_artist later.
    for idx in range(1000):
        ax.plot(np.arange(5000), label=idx)
    with rc_context({'legend.loc': 'best'}):
        legend = ax.legend()
    with pytest.warns(UserWarning) as records:
        fig.draw_artist(legend)  # Don't bother drawing the lines -- it's slow.
    # The _find_best_position method of Legend is called twice, duplicating
    # the warning message.
    assert len(records) == 2
    for record in records:
        assert str(record.message) == (
            'Creating legend with loc="best" can be slow with large '
            'amounts of data.')
