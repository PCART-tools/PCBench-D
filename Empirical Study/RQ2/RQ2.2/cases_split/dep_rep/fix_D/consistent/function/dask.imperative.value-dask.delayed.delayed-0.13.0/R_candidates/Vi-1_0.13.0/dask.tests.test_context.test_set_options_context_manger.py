def test_set_options_context_manger():
    with set_options(foo='bar'):
        assert _globals['foo'] == 'bar'
    assert _globals['foo'] is None

    try:
        set_options(foo='baz')
        assert _globals['foo'] == 'baz'
    finally:
        del _globals['foo']
