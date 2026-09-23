def test_invalid_layouts():
    fig, ax = plt.subplots(constrained_layout=True)
    with pytest.warns(UserWarning):
        # this should warn,
        fig.subplots_adjust(top=0.8)
    assert not(fig.get_constrained_layout())

    # Using layout + (tight|constrained)_layout warns, but the former takes
    # precedence.
    with pytest.warns(UserWarning, match="Figure parameters 'layout' and "
                      "'tight_layout' cannot"):
        fig = Figure(layout='tight', tight_layout=False)
    assert fig.get_tight_layout()
    assert not fig.get_constrained_layout()
    with pytest.warns(UserWarning, match="Figure parameters 'layout' and "
                      "'constrained_layout' cannot"):
        fig = Figure(layout='constrained', constrained_layout=False)
    assert not fig.get_tight_layout()
    assert fig.get_constrained_layout()

    with pytest.raises(ValueError,
                       match="'foobar' is not a valid value for layout"):
        Figure(layout='foobar')
