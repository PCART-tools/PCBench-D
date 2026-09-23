def test_chunks_is_immutable():
    x = da.ones(6, chunks=3)
    try:
        x.chunks = 2
        assert False
    except TypeError as e:
        assert 'rechunk(2)' in str(e)
