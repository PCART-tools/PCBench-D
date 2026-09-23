def test_get_dependencies_nothing():
    with pytest.raises(ValueError):
        get_dependencies({})
