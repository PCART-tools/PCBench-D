@pytest.mark.parametrize('label_array', [['low', 'high'],
                                         ('low', 'high'),
                                         np.array(['low', 'high'])])
def test_plot_single_input_multiple_label(label_array):
    # test ax.plot() with 1D array like input
    # and iterable label
    x = [1, 2, 3]
    y = [2, 5, 6]
    fig, ax = plt.subplots()
    ax.plot(x, y, label=label_array)
    leg = ax.legend()
    assert len(leg.get_texts()) == 1
    assert leg.get_texts()[0].get_text() == str(label_array)
