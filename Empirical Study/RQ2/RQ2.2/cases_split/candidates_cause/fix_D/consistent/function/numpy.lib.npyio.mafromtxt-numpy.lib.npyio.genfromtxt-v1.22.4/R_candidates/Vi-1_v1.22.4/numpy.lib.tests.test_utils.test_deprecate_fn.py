def test_deprecate_fn():
    assert_('old_func3' in new_func3.__doc__)
    assert_('new_func3' in new_func3.__doc__)
