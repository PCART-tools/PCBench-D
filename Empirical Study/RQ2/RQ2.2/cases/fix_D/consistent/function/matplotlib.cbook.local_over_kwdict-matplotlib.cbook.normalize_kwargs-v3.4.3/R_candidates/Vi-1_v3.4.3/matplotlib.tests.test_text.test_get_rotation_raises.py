def test_get_rotation_raises():
    with pytest.raises(ValueError):
        mpl.text.get_rotation('hozirontal')
