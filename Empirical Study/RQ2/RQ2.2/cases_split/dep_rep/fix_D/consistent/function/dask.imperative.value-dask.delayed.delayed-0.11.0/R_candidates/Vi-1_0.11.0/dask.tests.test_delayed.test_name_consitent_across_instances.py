def test_name_consitent_across_instances():
    func = delayed(identity, pure=True)

    data = {'x': 1, 'y': 25, 'z': [1, 2, 3]}
    if PY2:
        assert func(data)._key == 'identity-69e6d664a9054dce0e4dcaf48b919b8b'
    if PY3:
        assert func(data)._key == 'identity-6611a0dc9183f09b04a35db23d14fb7d'

    data = {'x': 1, 1: 'x'}
    assert func(data)._key == func(data)._key

    if PY2:
        assert func(1)._key == 'identity-9ed591b193ff79d4909cc7ae58786091'
    if PY3:
        assert func(1)._key == 'identity-1b6bde2fbd96b2278a4d2e7514366606'
