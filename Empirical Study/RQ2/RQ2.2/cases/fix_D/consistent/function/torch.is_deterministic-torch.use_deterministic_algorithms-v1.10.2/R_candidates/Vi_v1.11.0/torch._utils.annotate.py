def annotate(ret, **kwargs):
    def dec(fun):
        fun.__annotations__ = dict(kwargs)
        fun.__annotations__['return'] = ret
        return fun
    return dec
