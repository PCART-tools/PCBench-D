@register_lowering(aten.index, type_promotion_kind=None)
def index(x, indices):
    try:
        return index_impl(x, indices, check=True)
    except NotImplementedError:
        # Fallback to ATen for boolean indexing
        x.realize()
        return fallback_handler(aten.index.Tensor, add_to_fallback_set=False)(
            x, indices
        )
