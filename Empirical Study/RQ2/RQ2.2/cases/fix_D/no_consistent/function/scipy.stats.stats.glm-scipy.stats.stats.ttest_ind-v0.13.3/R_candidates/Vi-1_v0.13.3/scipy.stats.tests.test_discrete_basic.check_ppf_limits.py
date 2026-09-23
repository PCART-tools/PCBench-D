def check_ppf_limits(distfn,arg,msg):
    below,low,upp,above = distfn.ppf([-1,0,1,2], *arg)
    # print distfn.name, distfn.a, low, distfn.b, upp
    # print distfn.name,below,low,upp,above
    assert_equal_inf_nan(distfn.a-1,low, msg + 'ppf lower bound')
    assert_equal_inf_nan(distfn.b,upp, msg + 'ppf upper bound')
    npt.assert_(np.isnan(below), msg + 'ppf out of bounds - below')
    npt.assert_(np.isnan(above), msg + 'ppf out of bounds - above')
