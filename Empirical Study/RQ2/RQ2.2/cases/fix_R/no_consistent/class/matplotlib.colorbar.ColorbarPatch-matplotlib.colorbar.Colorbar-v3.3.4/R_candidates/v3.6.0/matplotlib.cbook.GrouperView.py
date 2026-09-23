class GrouperView:
    """Immutable view over a `.Grouper`."""

    def __init__(self, grouper):
        self._grouper = grouper

    class _GrouperMethodForwarder:
        def __init__(self, deprecated_kw=None):
            self._deprecated_kw = deprecated_kw

        def __set_name__(self, owner, name):
            wrapped = getattr(Grouper, name)
            forwarder = functools.wraps(wrapped)(
                lambda self, *args, **kwargs: wrapped(
                    self._grouper, *args, **kwargs))
            if self._deprecated_kw:
                forwarder = _api.deprecated(**self._deprecated_kw)(forwarder)
            setattr(owner, name, forwarder)

    __contains__ = _GrouperMethodForwarder()
    __iter__ = _GrouperMethodForwarder()
    joined = _GrouperMethodForwarder()
    get_siblings = _GrouperMethodForwarder()
    clean = _GrouperMethodForwarder(deprecated_kw=dict(since="3.6"))
    join = _GrouperMethodForwarder(deprecated_kw=dict(since="3.6"))
    remove = _GrouperMethodForwarder(deprecated_kw=dict(since="3.6"))
