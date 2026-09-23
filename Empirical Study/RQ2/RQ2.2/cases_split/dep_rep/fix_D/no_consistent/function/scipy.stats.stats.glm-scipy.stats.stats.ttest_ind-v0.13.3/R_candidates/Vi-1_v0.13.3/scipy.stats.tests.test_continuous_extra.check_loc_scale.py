def check_loc_scale(distfn,arg,msg):
    m,v = distfn.stats(*arg)
    loc, scale = 10.0, 10.0
    mt,vt = distfn.stats(loc=loc, scale=scale, *arg)
    assert_equal_inf_nan(m*scale+loc,mt,msg + 'mean')
    assert_equal_inf_nan(v*scale*scale,vt,msg + 'var')
