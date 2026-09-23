@pytest.mark.parametrize("badval", [-1, 3, None, "plate of shrimp"])
def test_bad_ndmin(badval):
    with pytest.raises(ValueError, match="Illegal value of ndmin keyword"):
        np.loadtxt("foo.bar", ndmin=badval)
