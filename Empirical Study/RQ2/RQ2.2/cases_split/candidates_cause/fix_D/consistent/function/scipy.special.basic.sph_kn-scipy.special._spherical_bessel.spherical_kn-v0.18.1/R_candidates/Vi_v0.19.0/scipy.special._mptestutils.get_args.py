def get_args(argspec, n):
    if isinstance(argspec, np.ndarray):
        args = argspec.copy()
    else:
        nargs = len(argspec)
        ms = np.asarray([1.5 if isinstance(spec, ComplexArg) else 1.0 for spec in argspec])
        ms = (n**(ms/sum(ms))).astype(int) + 1

        args = []
        for spec, m in zip(argspec, ms):
            args.append(spec.values(m))
        args = np.array(np.broadcast_arrays(*np.ix_(*args))).reshape(nargs, -1).T

    return args
