@register_lowering(inductor_prims._unsafe_index_put_, type_promotion_kind=None)
def _unsafe_index_put_(self, indices, values, accumulate=False):
    return index_put_impl_(
        self, indices, values, accumulate, check=False, may_realize=True
    )
