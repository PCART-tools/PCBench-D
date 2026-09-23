def test_uneven_chunks():
    assert da.ones(20, chunks=5)[::2].chunks == ((3, 2, 3, 2),)
