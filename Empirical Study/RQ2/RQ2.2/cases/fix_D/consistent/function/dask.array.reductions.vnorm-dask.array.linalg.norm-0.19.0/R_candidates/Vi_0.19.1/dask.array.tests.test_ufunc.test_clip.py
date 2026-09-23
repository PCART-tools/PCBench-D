def test_clip():
    x = np.random.normal(0, 10, size=(10, 10))
    d = da.from_array(x, chunks=(3, 4))

    assert_eq(x.clip(5), d.clip(5))
    assert_eq(x.clip(1, 5), d.clip(1, 5))
    assert_eq(x.clip(min=5), d.clip(min=5))
    assert_eq(x.clip(max=5), d.clip(max=5))
    assert_eq(x.clip(max=1, min=5), d.clip(max=1, min=5))
    assert_eq(x.clip(min=1, max=5), d.clip(min=1, max=5))
