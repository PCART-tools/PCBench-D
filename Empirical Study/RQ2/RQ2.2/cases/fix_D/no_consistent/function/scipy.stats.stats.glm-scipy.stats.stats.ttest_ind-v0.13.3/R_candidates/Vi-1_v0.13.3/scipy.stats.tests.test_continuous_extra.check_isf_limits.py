def check_isf_limits(distfn,arg,msg):
    below,low,upp,above = distfn.isf([-1,0,1,2], *arg)
    #print distfn.name, distfn.a, low, distfn.b, upp
    #print distfn.name,below,low,upp,above
    assert_equal_inf_nan(distfn.a,upp, msg + 'isf lower bound')
    assert_equal_inf_nan(distfn.b,low, msg + 'isf upper bound')
    npt.assert_(np.isnan(below), msg + 'isf out of bounds - below')
    npt.assert_(np.isnan(above), msg + 'isf out of bounds - above')
