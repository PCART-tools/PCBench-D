def test_bar_label_fmt():
    ax = plt.gca()
    rects = ax.bar([1, 2], [3, -4])
    labels = ax.bar_label(rects, fmt='%.2f')
    assert labels[0].get_text() == '3.00'
    assert labels[1].get_text() == '-4.00'
