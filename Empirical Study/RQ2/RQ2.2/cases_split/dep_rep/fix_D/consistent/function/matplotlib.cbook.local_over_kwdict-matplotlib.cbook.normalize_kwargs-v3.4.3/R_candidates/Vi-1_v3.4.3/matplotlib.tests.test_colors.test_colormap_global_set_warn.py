def test_colormap_global_set_warn():
    new_cm = plt.get_cmap('viridis')
    # Store the old value so we don't override the state later on.
    orig_cmap = copy.copy(new_cm)
    with pytest.warns(cbook.MatplotlibDeprecationWarning,
                      match="You are modifying the state of a globally"):
        # This should warn now because we've modified the global state
        new_cm.set_under('k')

    # This shouldn't warn because it is a copy
    copy.copy(new_cm).set_under('b')

    # Test that registering and then modifying warns
    plt.register_cmap(name='test_cm', cmap=copy.copy(orig_cmap))
    new_cm = plt.get_cmap('test_cm')
    with pytest.warns(cbook.MatplotlibDeprecationWarning,
                      match="You are modifying the state of a globally"):
        # This should warn now because we've modified the global state
        new_cm.set_under('k')

    # Re-register the original
    with pytest.warns(UserWarning):
        plt.register_cmap(cmap=orig_cmap, override_builtin=True)
