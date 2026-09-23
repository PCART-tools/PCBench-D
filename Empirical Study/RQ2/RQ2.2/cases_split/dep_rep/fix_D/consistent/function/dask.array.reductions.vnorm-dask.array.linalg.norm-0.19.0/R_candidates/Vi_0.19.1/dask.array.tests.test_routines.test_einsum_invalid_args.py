def test_einsum_invalid_args():
    _, da_inputs = _numpy_and_dask_inputs('a')
    with pytest.raises(TypeError):
        da.einsum('a', *da_inputs, foo=1, bar=2)
