def sph_harm_(m, n, theta, phi):
    y = sph_harm(m, n, theta, phi)
    return (y.real, y.imag)
