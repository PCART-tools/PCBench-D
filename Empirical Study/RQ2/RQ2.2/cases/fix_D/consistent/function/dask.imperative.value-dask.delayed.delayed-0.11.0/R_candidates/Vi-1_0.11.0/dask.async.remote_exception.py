def remote_exception(exc, tb):
    """ Metaclass that wraps exception type in RemoteException """
    if type(exc) in exceptions:
        typ = exceptions[type(exc)]
        return typ(exc, tb)
    else:
        try:
            typ = type(exc.__class__.__name__,
                       (RemoteException, type(exc)),
                       {'exception_type': type(exc)})
            exceptions[type(exc)] = typ
            return typ(exc, tb)
        except TypeError:
            return exc
