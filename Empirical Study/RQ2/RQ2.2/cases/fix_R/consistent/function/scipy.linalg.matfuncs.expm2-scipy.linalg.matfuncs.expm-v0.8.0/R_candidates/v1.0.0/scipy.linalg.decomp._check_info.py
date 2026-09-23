def _check_info(info, driver, positive='did not converge (LAPACK info=%d)'):
    """Check info return value."""
    if info < 0:
        raise ValueError('illegal value in argument %d of internal %s'
                         % (-info, driver))
    if info > 0 and positive:
        raise LinAlgError(("%s " + positive) % (driver, info,))
