def test_get_rotation_int():
    for i in [67, 16, 41]:
        assert mpl.text.get_rotation(i) == float(i)
