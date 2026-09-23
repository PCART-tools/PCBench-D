def test_deprecate_with_doc_decorator_message():
    assert_('Rather use new_func7' in old_func7.__doc__)
