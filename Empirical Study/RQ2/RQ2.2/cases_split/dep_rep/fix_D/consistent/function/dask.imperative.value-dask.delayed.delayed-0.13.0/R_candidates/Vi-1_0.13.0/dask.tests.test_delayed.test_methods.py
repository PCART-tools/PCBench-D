def test_methods():
    a = delayed("a b c d e")
    assert a.split(' ').compute() == ['a', 'b', 'c', 'd', 'e']
    assert a.upper().replace('B', 'A').split().count('A').compute() == 2
    assert a.split(' ', pure=True).key == a.split(' ', pure=True).key
    o = a.split(' ', dask_key_name='test')
    assert o.key == 'test'
