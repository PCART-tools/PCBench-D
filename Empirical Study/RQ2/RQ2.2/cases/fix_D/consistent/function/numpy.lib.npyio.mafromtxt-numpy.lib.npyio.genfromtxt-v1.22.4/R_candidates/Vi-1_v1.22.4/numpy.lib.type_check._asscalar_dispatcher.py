def _asscalar_dispatcher(a):
    # 2018-10-10, 1.16
    warnings.warn('np.asscalar(a) is deprecated since NumPy v1.16, use '
                  'a.item() instead', DeprecationWarning, stacklevel=3)
    return (a,)
