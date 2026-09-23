def test_sph_harm():
    # Tests derived from tables in
    # http://en.wikipedia.org/wiki/Table_of_spherical_harmonics
    sh = special.sph_harm
    pi = np.pi
    exp = np.exp
    sqrt = np.sqrt
    sin = np.sin
    cos = np.cos
    yield (assert_array_almost_equal, sh(0,0,0,0),
           0.5/sqrt(pi))
    yield (assert_array_almost_equal, sh(-2,2,0.,pi/4),
           0.25*sqrt(15./(2.*pi)) *
           (sin(pi/4))**2.)
    yield (assert_array_almost_equal, sh(-2,2,0.,pi/2),
           0.25*sqrt(15./(2.*pi)))
    yield (assert_array_almost_equal, sh(2,2,pi,pi/2),
           0.25*sqrt(15/(2.*pi)) *
           exp(0+2.*pi*1j)*sin(pi/2.)**2.)
    yield (assert_array_almost_equal, sh(2,4,pi/4.,pi/3.),
           (3./8.)*sqrt(5./(2.*pi)) *
           exp(0+2.*pi/4.*1j) *
           sin(pi/3.)**2. *
           (7.*cos(pi/3.)**2.-1))
    yield (assert_array_almost_equal, sh(4,4,pi/8.,pi/6.),
           (3./16.)*sqrt(35./(2.*pi)) *
           exp(0+4.*pi/8.*1j)*sin(pi/6.)**4.)
