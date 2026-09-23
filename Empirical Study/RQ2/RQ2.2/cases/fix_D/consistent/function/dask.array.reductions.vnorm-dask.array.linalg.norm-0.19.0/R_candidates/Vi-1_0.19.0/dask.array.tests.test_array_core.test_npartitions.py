def test_npartitions():
    assert da.ones(5, chunks=(2,)).npartitions == 3
    assert da.ones((5, 5), chunks=(2, 3)).npartitions == 6
