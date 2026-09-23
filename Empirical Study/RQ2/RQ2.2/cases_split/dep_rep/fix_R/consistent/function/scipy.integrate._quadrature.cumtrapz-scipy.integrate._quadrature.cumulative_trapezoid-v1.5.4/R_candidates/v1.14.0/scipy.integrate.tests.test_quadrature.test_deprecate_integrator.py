@pytest.mark.parametrize('func', [romberg, quadrature])
def test_deprecate_integrator(func):
    message = f"`scipy.integrate.{func.__name__}` is deprecated..."
    with pytest.deprecated_call(match=message):
        func(np.exp, 0, 1)
