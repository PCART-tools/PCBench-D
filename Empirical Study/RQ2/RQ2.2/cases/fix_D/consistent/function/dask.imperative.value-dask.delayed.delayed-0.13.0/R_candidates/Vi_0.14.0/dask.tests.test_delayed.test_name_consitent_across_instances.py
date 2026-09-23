def test_name_consitent_across_instances():
    func = delayed(identity, pure=True)

    data = {'x': 1, 'y': 25, 'z': [1, 2, 3]}
    if PY2:
        assert func(data)._key == 'identity-6700b857eea9a7d3079762c9a253ffbd'
    if PY3:
        assert func(data)._key == 'identity-84c5e2194036c17d1d97c4e3a2b90482'

    data = {'x': 1, 1: 'x'}
    assert func(data)._key == func(data)._key

    if PY2:
        assert func(1)._key == 'identity-91f02358e13dca18cde218a63fee436a'
    if PY3:
        assert func(1)._key == 'identity-7126728842461bf3d2caecf7b954fa3b'
