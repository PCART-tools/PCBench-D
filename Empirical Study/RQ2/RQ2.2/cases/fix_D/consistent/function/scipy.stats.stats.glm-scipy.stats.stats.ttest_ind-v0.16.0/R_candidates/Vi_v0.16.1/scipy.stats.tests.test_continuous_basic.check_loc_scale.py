@npt.dec.skipif(NUMPY_BELOW_1_7)
def check_loc_scale(distfn, arg, m, v, msg):
    loc, scale = 10.0, 10.0
    mt, vt = distfn.stats(loc=loc, scale=scale, *arg)
    npt.assert_allclose(m*scale + loc, mt)
    npt.assert_allclose(v*scale*scale, vt)
