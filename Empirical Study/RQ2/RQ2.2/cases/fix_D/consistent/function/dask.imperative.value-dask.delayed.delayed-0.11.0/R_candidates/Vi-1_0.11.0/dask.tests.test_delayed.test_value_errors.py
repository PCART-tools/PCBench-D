def test_value_errors():
    a = delayed([1, 2, 3])
    # Immutable
    assert raises(TypeError, lambda: setattr(a, 'foo', 1))
    assert raises(TypeError, lambda: setattr(a, '_key', 'test'))
    assert raises(TypeError, lambda: setitem(a, 1, 0))
    # Can't iterate, or check if contains
    assert raises(TypeError, lambda: 1 in a)
    assert raises(TypeError, lambda: list(a))
    # No dynamic generation of magic methods
    assert raises(AttributeError, lambda: a.__len__())
    # Truth of values forbidden
    assert raises(TypeError, lambda: bool(a))
