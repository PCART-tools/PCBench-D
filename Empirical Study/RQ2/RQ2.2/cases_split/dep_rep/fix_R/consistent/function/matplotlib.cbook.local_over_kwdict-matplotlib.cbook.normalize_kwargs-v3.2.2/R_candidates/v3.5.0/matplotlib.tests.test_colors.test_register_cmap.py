def test_register_cmap():
    new_cm = copy.copy(cm.get_cmap("viridis"))
    target = "viridis2"
    cm.register_cmap(target, new_cm)
    assert plt.get_cmap(target) == new_cm

    with pytest.raises(ValueError,
                       match="Arguments must include a name or a Colormap"):
        cm.register_cmap()

    with pytest.warns(UserWarning):
        cm.register_cmap(target, new_cm)

    cm.unregister_cmap(target)
    with pytest.raises(ValueError,
                       match=f'{target!r} is not a valid value for name;'):
        cm.get_cmap(target)
    # test that second time is error free
    cm.unregister_cmap(target)

    with pytest.raises(ValueError, match="You must pass a Colormap instance."):
        cm.register_cmap('nome', cmap='not a cmap')
