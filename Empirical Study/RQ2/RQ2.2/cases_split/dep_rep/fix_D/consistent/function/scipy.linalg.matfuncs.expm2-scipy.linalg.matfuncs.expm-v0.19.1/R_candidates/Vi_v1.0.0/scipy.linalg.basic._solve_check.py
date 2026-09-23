def _solve_check(n, info, lamch=None, rcond=None):
    """ Check arguments during the different steps of the solution phase """
    if info < 0:
        raise ValueError('LAPACK reported an illegal value in {}-th argument'
                         '.'.format(-info))
    elif 0 < info:
        raise LinAlgError('Matrix is singular.')

    if lamch is None:
        return
    E = lamch('E')
    if rcond < E:
        warnings.warn('scipy.linalg.solve\nIll-conditioned matrix detected.'
                      ' Result is not guaranteed to be accurate.\nReciprocal '
                      'condition number/precision: {} / {}'.format(rcond, E),
                      RuntimeWarning)
