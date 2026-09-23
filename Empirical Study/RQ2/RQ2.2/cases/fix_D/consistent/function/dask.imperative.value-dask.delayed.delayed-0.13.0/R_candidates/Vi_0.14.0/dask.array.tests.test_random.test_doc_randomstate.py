def test_doc_randomstate():
    assert 'mean' in da.random.RandomState(5).normal.__doc__
