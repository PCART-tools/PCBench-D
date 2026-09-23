def test_hinting_factor_backends():
    plt.rcParams['text.hinting_factor'] = 1
    fig = plt.figure()
    t = fig.text(0.5, 0.5, 'some text')

    fig.savefig(io.BytesIO(), format='svg')
    expected = t.get_window_extent().intervalx

    fig.savefig(io.BytesIO(), format='png')
    # Backends should apply hinting_factor consistently (within 10%).
    np.testing.assert_allclose(t.get_window_extent().intervalx, expected,
                               rtol=0.1)
