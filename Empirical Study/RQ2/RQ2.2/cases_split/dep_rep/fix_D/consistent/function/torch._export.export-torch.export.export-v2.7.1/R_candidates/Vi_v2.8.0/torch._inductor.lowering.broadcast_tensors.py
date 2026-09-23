@register_lowering(aten.broadcast_tensors, broadcast=False, type_promotion_kind=None)
def broadcast_tensors(*inputs):
    if len(inputs) == 1 and isinstance(inputs[0], (list, tuple)):
        return broadcast_tensors(*inputs[0])
    target: list[sympy.Expr] = functools.reduce(
        broadcast_symbolic_shapes, [x.get_size() for x in inputs], []
    )
    outputs = []
    for x in inputs:
        sizes = x.get_size()
        if len(sizes) != len(target) or any(
            (
                (
                    V.graph.sizevars.shape_env.evaluate_expr(
                        sympy.Eq(a, 1), size_oblivious=True
                    )
                    and not V.graph.sizevars.shape_env.evaluate_expr(
                        sympy.Eq(b, 1), size_oblivious=True
                    )
                )
                or (
                    not V.graph.sizevars.shape_env.evaluate_expr(
                        sympy.Eq(a, 1), size_oblivious=True
                    )
                    and V.graph.sizevars.shape_env.evaluate_expr(
                        sympy.Eq(b, 1), size_oblivious=True
                    )
                )
            )
            for a, b in zip(sizes, target)
        ):
            x = expand(x, target)
        outputs.append(x)
    return outputs
