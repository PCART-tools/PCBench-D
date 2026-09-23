@register_lowering(aten.index_put_, type_promotion_kind=None)
def index_put_(self, indices, values, accumulate=False):
    return index_put_impl_(
        self, indices, values, accumulate, check=True, may_realize=True
    )
