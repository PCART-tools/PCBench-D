@pytest.mark.parametrize('einsum_signature', [
    'abc,bad->abcd',
    'abcdef,bcdfg->abcdeg',
    'ea,fb,abcd,gc,hd->efgh',
    'ab,b',
    'aa',
    'a,a->',
    'a,a->a',
    'a,a',
    'a,b',
    'a,b,c',
    'a',
    'ba,b',
    'ba,b->',
    'defab,fedbc->defac',
    'ab...,bc...->ac...',
    'a...a',
    'abc...->cba...',
    '...ab->...a',
    'a...a->a...',
    # Following 2 from # https://stackoverflow.com/a/19203475/1611416
    '...abc,...abcd->...d',
    'ab...,b->ab...',
    # https://github.com/dask/dask/pull/3412#discussion_r182413444
    'aa->a',
    'ab,ab,c->c',
    'aab,bc->ac',
    'aab,bcc->ac',
    'fdf,cdd,ccd,afe->ae',
    'fff,fae,bef,def->abd',
])
def test_einsum(einsum_signature):
    input_sigs = (einsum_signature.split('->')[0]
                                  .replace("...", "*")
                                  .split(','))

    np_inputs, da_inputs = _numpy_and_dask_inputs(input_sigs)

    with pytest.warns(None):
        assert_eq(np.einsum(einsum_signature, *np_inputs),
                  da.einsum(einsum_signature, *da_inputs))
