def test__parse_gufunc_signature():
    assert_equal(_parse_gufunc_signature('(x)->()'), ([('x',)], ()))
    assert_equal(_parse_gufunc_signature('(x,y)->()'),
                 ([('x', 'y')], ()))
    assert_equal(_parse_gufunc_signature('(x),(y)->()'),
                 ([('x',), ('y',)], ()))
    assert_equal(_parse_gufunc_signature('(x)->(y)'),
                 ([('x',)], ('y',)))
    assert_equal(_parse_gufunc_signature('(x)->(y),()'),
                 ([('x',)], [('y',), ()]))
    assert_equal(_parse_gufunc_signature('(),(a,b,c),(d)->(d,e)'),
                 ([(), ('a', 'b', 'c'), ('d',)], ('d', 'e')))
    with pytest.raises(ValueError):
        _parse_gufunc_signature('(x)(y)->()')
    with pytest.raises(ValueError):
        _parse_gufunc_signature('(x),(y)->')
    with pytest.raises(ValueError):
        _parse_gufunc_signature('((x))->(x)')
    with pytest.raises(ValueError):
        _parse_gufunc_signature('(x)->(x),')
