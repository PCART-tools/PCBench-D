def test_skew_raises():
    a = da.ones((7,), chunks=(7,))
    with pytest.raises(ValueError) as rec:
        dask.array.stats.skewtest(a)

    assert "7 samples" in str(rec)
