def seed(seed=None):
    """
    Seed the internal random number generator used in this ID package.

    The generator is a lagged Fibonacci method with 55-element internal state.

    Parameters
    ----------
    seed : int, sequence, 'default', optional
        If 'default', the random seed is reset to a default value.

        If `seed` is a sequence containing 55 floating-point numbers
        in range [0,1], these are used to set the internal state of
        the generator.

        If the value is an integer, the internal state is obtained
        from `numpy.random.RandomState` (MT19937) with the integer
        used as the initial seed.

        If `seed` is omitted (None), `numpy.random` is used to
        initialize the generator.

    """
    # For details, see :func:`backend.id_srand`, :func:`backend.id_srandi`,
    # and :func:`backend.id_srando`.

    if isinstance(seed, str) and seed == 'default':
        backend.id_srando()
    elif hasattr(seed, '__len__'):
        state = np.asfortranarray(seed, dtype=float)
        if state.shape != (55,):
            raise ValueError("invalid input size")
        elif state.min() < 0 or state.max() > 1:
            raise ValueError("values not in range [0,1]")
        backend.id_srandi(state)
    elif seed is None:
        backend.id_srandi(np.random.rand(55))
    else:
        rnd = np.random.RandomState(seed)
        backend.id_srandi(rnd.rand(55))
