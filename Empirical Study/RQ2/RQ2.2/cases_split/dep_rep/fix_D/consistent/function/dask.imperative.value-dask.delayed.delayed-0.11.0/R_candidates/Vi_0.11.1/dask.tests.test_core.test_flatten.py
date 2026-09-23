def test_flatten():
    assert list(flatten(())) == []
    assert list(flatten('foo')) == ['foo']
