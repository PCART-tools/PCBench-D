@register_lowering(torch.ops.higher_order.while_loop, type_promotion_kind=None)
def while_loop(cond_fn, body_fn, carried_inputs, additional_inputs):
    if any(
        isinstance(x, IRNode) and is_triton(x)
        for x in carried_inputs + additional_inputs
    ):
        msg = "control flow operator: torch.while_loop."
        if stack_trace := V.graph.current_node.meta.get("stack_trace", None):
            msg = f"{msg} Found from : \n {stack_trace}"
        V.graph.disable_cudagraphs_reason = msg

    def _map_output(out: Any):
        if isinstance(out, TensorBox):
            return out
        elif isinstance(out, ir.StorageBox):
            return TensorBox(out)
        elif isinstance(out, ir.MultiOutput):
            return TensorBox.create(out)
        else:
            raise RuntimeError(f"NYI unsupported output type: {type(out)}")

    result = ir.WhileLoop.create(cond_fn, body_fn, carried_inputs, additional_inputs)
    return list(map(_map_output, result))
