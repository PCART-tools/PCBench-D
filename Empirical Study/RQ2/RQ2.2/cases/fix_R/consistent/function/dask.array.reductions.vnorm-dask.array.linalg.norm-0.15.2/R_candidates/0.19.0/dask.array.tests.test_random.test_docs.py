def test_docs():
    assert 'exponential' in exponential.__doc__
    assert 'exponential' in exponential.__name__
    assert "# doctest: +SKIP" in normal.__doc__
