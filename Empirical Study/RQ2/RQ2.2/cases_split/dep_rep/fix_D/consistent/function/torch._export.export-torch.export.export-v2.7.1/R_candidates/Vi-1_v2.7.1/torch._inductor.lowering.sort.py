@register_lowering(aten.sort.default, type_promotion_kind=None)
def sort(x, dim=-1, descending=False):
    return sort_stable(x, stable=False, dim=dim, descending=descending)
