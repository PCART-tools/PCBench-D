@register_lowering(torch.ops.higher_order.with_effects, type_promotion_kind=None)
def with_effects(token, op, *args, **kwargs):
    result = ir.EffectfulKernel.create(op, *args, **kwargs)

    from torch._higher_order_ops.effects import get_effect_key

    effect_type = get_effect_key(op, args, kwargs)
    assert effect_type is not None
    effectful_kernel = V.graph.effectful_ops[effect_type]

    if result is None:
        return (effectful_kernel,)

    result = pytree.tree_map_only(ir.MultiOutput, TensorBox.create, result)
    if not isinstance(result, (list, tuple)):
        return (effectful_kernel, result)
    else:
        return (effectful_kernel, *result)
