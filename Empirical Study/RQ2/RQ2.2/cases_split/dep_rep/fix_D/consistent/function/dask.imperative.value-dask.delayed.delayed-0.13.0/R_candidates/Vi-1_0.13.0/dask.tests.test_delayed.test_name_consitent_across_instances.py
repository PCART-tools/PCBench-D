def test_name_consitent_across_instances():
    func = delayed(identity, pure=True)

    data = {'x': 1, 'y': 25, 'z': [1, 2, 3]}
    if PY2:
        assert func(data)._key == 'identity-777036d61a8334229dc0eda4454830d7'
    if PY3:
        assert func(data)._key == 'identity-1de4057b4cfa0ba7faed76b9c383cc99'

    data = {'x': 1, 1: 'x'}
    assert func(data)._key == func(data)._key

    if PY2:
        assert func(1)._key == 'identity-d3eda9ebeead15c7e491960e89605b7f'
    if PY3:
        assert func(1)._key == 'identity-5390b9efe3ddb6ea0557139003eef253'
