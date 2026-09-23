def test_delayed_errors():
    a = delayed([1, 2, 3])
    # Immutable
    pytest.raises(TypeError, lambda: setattr(a, 'foo', 1))
    pytest.raises(TypeError, lambda: setitem(a, 1, 0))
    # Can't iterate, or check if contains
    pytest.raises(TypeError, lambda: 1 in a)
    pytest.raises(TypeError, lambda: list(a))
    # No dynamic generation of magic/hidden methods
    pytest.raises(AttributeError, lambda: a._hidden())
    # Truth of delayed forbidden
    pytest.raises(TypeError, lambda: bool(a))
