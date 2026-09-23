def test_norm_callback():
    increment = unittest.mock.Mock(return_value=None)

    norm = mcolors.Normalize()
    norm.callbacks.connect('changed', increment)
    # Haven't updated anything, so call count should be 0
    assert increment.call_count == 0

    # Now change vmin and vmax to test callbacks
    norm.vmin = 1
    assert increment.call_count == 1
    norm.vmax = 5
    assert increment.call_count == 2
    # callback shouldn't be called if setting to the same value
    norm.vmin = 1
    assert increment.call_count == 2
    norm.vmax = 5
    assert increment.call_count == 2
