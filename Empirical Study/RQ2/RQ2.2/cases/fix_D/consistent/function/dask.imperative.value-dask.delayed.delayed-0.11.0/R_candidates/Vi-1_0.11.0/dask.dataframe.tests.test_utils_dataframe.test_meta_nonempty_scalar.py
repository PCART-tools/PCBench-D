def test_meta_nonempty_scalar():
    meta = meta_nonempty(np.float64(1.0))
    assert isinstance(meta, np.float64)

    x = pd.Timestamp(2000, 1, 1)
    meta = meta_nonempty(x)
    assert meta is x
