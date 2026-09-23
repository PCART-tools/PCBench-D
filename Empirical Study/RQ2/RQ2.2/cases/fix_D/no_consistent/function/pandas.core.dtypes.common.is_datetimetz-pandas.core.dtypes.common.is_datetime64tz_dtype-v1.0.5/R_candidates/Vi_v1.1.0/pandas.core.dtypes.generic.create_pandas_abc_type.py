def create_pandas_abc_type(name, attr, comp):

    # https://github.com/python/mypy/issues/1006
    # error: 'classmethod' used with a non-method
    @classmethod  # type: ignore
    def _check(cls, inst) -> bool:
        return getattr(inst, attr, "_typ") in comp

    dct = dict(__instancecheck__=_check, __subclasscheck__=_check)
    meta = type("ABCBase", (type,), dct)
    return meta(name, tuple(), dct)
