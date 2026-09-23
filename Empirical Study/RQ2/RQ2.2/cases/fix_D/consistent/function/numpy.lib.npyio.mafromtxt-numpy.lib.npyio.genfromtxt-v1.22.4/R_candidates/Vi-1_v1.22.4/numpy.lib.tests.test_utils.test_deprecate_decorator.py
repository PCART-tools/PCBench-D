def test_deprecate_decorator():
    assert_('deprecated' in old_func.__doc__)
