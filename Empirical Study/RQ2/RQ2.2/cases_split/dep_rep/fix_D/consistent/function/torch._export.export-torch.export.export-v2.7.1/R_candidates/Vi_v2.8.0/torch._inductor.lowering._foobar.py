@register_lowering(aten._foobar)
def _foobar(_):
    raise AssertionError
