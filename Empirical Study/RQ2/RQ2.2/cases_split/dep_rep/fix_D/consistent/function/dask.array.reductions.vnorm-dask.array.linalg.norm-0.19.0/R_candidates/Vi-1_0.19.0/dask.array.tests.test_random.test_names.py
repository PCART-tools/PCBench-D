def test_names():
    name = da.random.normal(0, 1, size=(1000,), chunks=(500,)).name

    assert name.startswith('normal')
    assert len(key_split(name)) < 10
