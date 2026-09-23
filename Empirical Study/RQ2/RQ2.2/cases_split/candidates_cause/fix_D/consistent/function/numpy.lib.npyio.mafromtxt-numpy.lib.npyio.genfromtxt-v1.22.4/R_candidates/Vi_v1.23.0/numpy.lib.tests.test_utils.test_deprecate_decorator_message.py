def test_deprecate_decorator_message():
    assert_('Rather use new_func2' in old_func2.__doc__)
