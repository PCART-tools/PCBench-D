@register_lowering(aten.index_put)
def index_put(x, indices, values, accumulate=False):
    return index_put_impl_(
        clone(x), indices, values, accumulate, check=True, may_realize=False
    )
