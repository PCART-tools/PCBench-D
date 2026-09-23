def assert_wolfe(s, phi, derphi, c1=1e-4, c2=0.9, err_msg=""):
    """
    Check that strong Wolfe conditions apply
    """
    phi1 = phi(s)
    phi0 = phi(0)
    derphi0 = derphi(0)
    derphi1 = derphi(s)
    msg = "s = %s; phi(0) = %s; phi(s) = %s; phi'(0) = %s; phi'(s) = %s; %s" % (
        s, phi0, phi1, derphi0, derphi1, err_msg)

    assert_(phi1 <= phi0 + c1*s*derphi0, "Wolfe 1 failed: " + msg)
    assert_(abs(derphi1) <= abs(c2*derphi0), "Wolfe 2 failed: " + msg)
