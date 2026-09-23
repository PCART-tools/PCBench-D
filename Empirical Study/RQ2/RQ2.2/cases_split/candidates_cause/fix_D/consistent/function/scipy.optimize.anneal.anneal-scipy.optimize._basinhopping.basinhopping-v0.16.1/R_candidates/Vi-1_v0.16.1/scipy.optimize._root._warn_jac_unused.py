def _warn_jac_unused(jac, method):
    if jac is not None:
        warn('Method %s does not use the jacobian (jac).' % (method,),
             RuntimeWarning)
