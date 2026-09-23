@register_lowering(torch.ops.higher_order.cond, type_promotion_kind=None)
def cond(pred, true_fn, false_fn, operands):
    if any(isinstance(x, IRNode) and is_triton(x) for x in [pred, *operands]):
        msg = "control flow operator: torch.cond."
        if stack_trace := V.graph.current_node.meta.get("stack_trace", None):
            msg = f"{msg} Found from : \n {stack_trace}"
        V.graph.disable_cudagraphs_reason = msg

    result = ir.Conditional.create(pred, true_fn, false_fn, operands)
    return list(map(TensorBox.create, result))
