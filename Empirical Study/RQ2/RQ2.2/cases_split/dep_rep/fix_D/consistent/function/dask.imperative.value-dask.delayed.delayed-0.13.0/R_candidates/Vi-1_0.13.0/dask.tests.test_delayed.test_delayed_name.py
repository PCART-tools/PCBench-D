def test_delayed_name():
    assert delayed(1)._key.startswith('int-')
    assert delayed(1, pure=True)._key.startswith('int-')
    assert delayed(1, name='X')._key == 'X'

    def myfunc(x):
        return x + 1

    assert delayed(myfunc)(1).key.startswith('myfunc')
