@pytest.mark.parametrize('casting', [
    'no', 'equiv', 'safe', 'same_kind', 'unsafe'])
def test_einsum_casting(casting):
    sig = 'ea,fb,abcd,gc,hd->efgh'
    input_sigs = sig.split('->')[0].split(',')
    np_inputs, da_inputs = _numpy_and_dask_inputs(input_sigs)

    assert_eq(np.einsum(sig, *np_inputs, casting=casting),
              da.einsum(sig, *np_inputs, casting=casting))
