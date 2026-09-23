        def __set_name__(self, owner, name):
            wrapped = getattr(Grouper, name)
            forwarder = functools.wraps(wrapped)(
                lambda self, *args, **kwargs: wrapped(
                    self._grouper, *args, **kwargs))
            if self._deprecated_kw:
                forwarder = _api.deprecated(**self._deprecated_kw)(forwarder)
            setattr(owner, name, forwarder)
