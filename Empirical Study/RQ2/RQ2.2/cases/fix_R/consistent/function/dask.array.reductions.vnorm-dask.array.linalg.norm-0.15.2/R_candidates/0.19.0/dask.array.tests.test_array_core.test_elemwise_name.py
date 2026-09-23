def test_elemwise_name():
    assert (da.ones(5, chunks=2) + 1).name.startswith('add-')
