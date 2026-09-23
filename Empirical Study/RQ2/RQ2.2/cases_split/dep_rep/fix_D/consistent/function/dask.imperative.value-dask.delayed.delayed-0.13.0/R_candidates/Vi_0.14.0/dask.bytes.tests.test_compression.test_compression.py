def test_compression():
    assert set(compress) == set(decompress)

    a = b'Hello, world!'
    for k in compress:
        comp = compress[k]
        decomp = decompress[k]
        b = comp(a)
        c = decomp(b)
        assert a == c
        if k is not None:
            assert a != b
