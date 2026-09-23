@pytest.mark.parametrize('order', ['C', 'F', 'A', 'K'])
def test_einsum_order(order):
    sig = 'ea,fb,abcd,gc,hd->efgh'
    input_sigs = sig.split('->')[0].split(',')
    np_inputs, da_inputs = _numpy_and_dask_inputs(input_sigs)

    assert_eq(np.einsum(sig, *np_inputs, order=order),
              da.einsum(sig, *np_inputs, order=order))
