@register_lowering(aten._foobar)
def foobar(self, *args, **kwargs):
    raise NotImplementedError("Helpful for debugging")
