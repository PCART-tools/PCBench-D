def test_double_register_builtin_cmap():
    name = "viridis"
    match = f"Trying to re-register the builtin cmap {name!r}."
    with pytest.raises(ValueError, match=match):
        cm.register_cmap(name, cm.get_cmap(name))
    with pytest.warns(UserWarning):
        cm.register_cmap(name, cm.get_cmap(name), override_builtin=True)
