def test_get_rotation_string():
    assert mpl.text.get_rotation('horizontal') == 0.
    assert mpl.text.get_rotation('vertical') == 90.
    assert mpl.text.get_rotation('15.') == 15.
