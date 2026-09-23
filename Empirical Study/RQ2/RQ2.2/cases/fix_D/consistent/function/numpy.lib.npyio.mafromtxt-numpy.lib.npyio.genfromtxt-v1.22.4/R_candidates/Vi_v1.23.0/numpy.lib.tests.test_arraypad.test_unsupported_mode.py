@pytest.mark.parametrize("mode", [1, "const", object(), None, True, False])
def test_unsupported_mode(mode):
    match= "mode '{}' is not supported".format(mode)
    with pytest.raises(ValueError, match=match):
        np.pad([1, 2, 3], 4, mode=mode)
