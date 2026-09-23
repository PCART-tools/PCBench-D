@pytest.mark.skipif(not einsum_can_optimize,
                    reason="np.einsum(optimize) unavailable")
@pytest.mark.parametrize('optimize_opts', [
    (True, False),
    ('greedy', False),
    ('optimal', False)
])
def test_einsum_optimize(optimize_opts):
    sig = 'ea,fb,abcd,gc,hd->efgh'
    input_sigs = sig.split('->')[0].split(',')
    np_inputs, da_inputs = _numpy_and_dask_inputs(input_sigs)

    opt1, opt2 = optimize_opts

    assert_eq(np.einsum(sig, *np_inputs, optimize=opt1),
              da.einsum(sig, *np_inputs, optimize=opt2))

    assert_eq(np.einsum(sig, *np_inputs, optimize=opt2),
              da.einsum(sig, *np_inputs, optimize=opt1))
