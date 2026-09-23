def test_warn_cl_plus_tl():
    fig, ax = plt.subplots(constrained_layout=True)
    with pytest.warns(UserWarning):
        # this should warn,
        fig.subplots_adjust(top=0.8)
    assert not(fig.get_constrained_layout())
