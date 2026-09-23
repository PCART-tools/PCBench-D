def test_exceptions():
    # TODO should this test more options?
    with pytest.raises(ValueError):
        plt.subplots(2, 2, sharex='blah')
    with pytest.raises(ValueError):
        plt.subplots(2, 2, sharey='blah')
    # We filter warnings in this test which are genuine since
    # the point of this test is to ensure that this raises.
    with pytest.warns(UserWarning, match='.*sharex argument to subplots'), \
         pytest.raises(ValueError):
        plt.subplots(2, 2, -1)
    with pytest.warns(UserWarning, match='.*sharex argument to subplots'), \
         pytest.raises(ValueError):
        plt.subplots(2, 2, 0)
    with pytest.warns(UserWarning, match='.*sharex argument to subplots'), \
         pytest.raises(ValueError):
        plt.subplots(2, 2, 5)
