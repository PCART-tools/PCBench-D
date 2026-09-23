def test_rcparams_init():
    with pytest.raises(ValueError), \
         pytest.warns(UserWarning, match="validate"):
        mpl.RcParams({'figure.figsize': (3.5, 42, 1)})
