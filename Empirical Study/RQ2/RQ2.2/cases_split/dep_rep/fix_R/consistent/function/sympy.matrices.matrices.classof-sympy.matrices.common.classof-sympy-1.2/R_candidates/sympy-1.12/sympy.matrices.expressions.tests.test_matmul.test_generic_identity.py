def test_generic_identity():
    assert MatMul.identity == GenericIdentity()
    assert MatMul.identity != S.One
