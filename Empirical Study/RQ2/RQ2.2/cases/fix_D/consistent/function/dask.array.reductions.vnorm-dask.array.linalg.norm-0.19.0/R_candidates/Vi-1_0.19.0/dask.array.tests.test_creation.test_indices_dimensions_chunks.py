def test_indices_dimensions_chunks():
    chunks = ((1,4,2,3), (5,5))
    darr = da.indices((10, 10), chunks=chunks)
    assert darr.chunks == ((1,1),) + chunks
