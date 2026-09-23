def test_get_rotation_float():
    for i in [15., 16.70, 77.4]:
        assert mpl.text.get_rotation(i) == i
