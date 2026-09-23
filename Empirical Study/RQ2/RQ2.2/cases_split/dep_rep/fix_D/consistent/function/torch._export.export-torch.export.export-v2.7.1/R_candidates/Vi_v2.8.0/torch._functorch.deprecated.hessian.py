def hessian(func, argnums=0):
    warn_deprecated("hessian")
    return _impl.hessian(func, argnums=argnums)
