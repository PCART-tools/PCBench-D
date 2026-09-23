def test_unregister_builtin_cmap():
    name = "viridis"
    match = f'cannot unregister {name!r} which is a builtin colormap.'
    with pytest.raises(ValueError, match=match):
        cm.unregister_cmap(name)
