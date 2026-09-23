def test_delayed_name_on_call():
    f = delayed(add, pure=True)
    assert f(1, 2, dask_key_name='foo')._key == 'foo'
