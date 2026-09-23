def test_bar_label_location_center():
    ax = plt.gca()
    ys, widths = [1, 2], [3, -4]
    rects = ax.barh(ys, widths)
    labels = ax.bar_label(rects, label_type='center')
    assert labels[0].xy == (widths[0] / 2, ys[0])
    assert labels[0].get_ha() == 'center'
    assert labels[0].get_va() == 'center'
    assert labels[1].xy == (widths[1] / 2, ys[1])
    assert labels[1].get_ha() == 'center'
    assert labels[1].get_va() == 'center'
