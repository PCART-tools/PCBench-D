@register_lowering(aten.native_dropout, type_promotion_kind=None)
def native_dropout(x, p, train):
    if config.fallback_random:
        return pytree.tree_map(
            TensorBox.create,
            ir.FallbackKernel.create(aten.native_dropout.default, x, p, train),
        )
    else:
        raise AssertionError("should be handled in replace_random.py")
