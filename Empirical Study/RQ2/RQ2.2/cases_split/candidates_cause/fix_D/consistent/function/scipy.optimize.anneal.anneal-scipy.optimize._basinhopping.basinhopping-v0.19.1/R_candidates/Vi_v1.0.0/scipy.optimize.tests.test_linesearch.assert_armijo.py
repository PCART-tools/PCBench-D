def assert_armijo(s, phi, c1=1e-4, err_msg=""):
    """
    Check that Armijo condition applies
    """
    phi1 = phi(s)
    phi0 = phi(0)
    msg = "s = %s; phi(0) = %s; phi(s) = %s; %s" % (s, phi0, phi1, err_msg)
    assert_(phi1 <= (1 - c1*s)*phi0, msg)
