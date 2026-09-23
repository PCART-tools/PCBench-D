@pytest.mark.parametrize('split_every', [None, 2])
def test_einsum_split_every(split_every):
    np_inputs, da_inputs = _numpy_and_dask_inputs('a')
    assert_eq(np.einsum('a', *np_inputs),
              da.einsum('a', *da_inputs, split_every=split_every))
