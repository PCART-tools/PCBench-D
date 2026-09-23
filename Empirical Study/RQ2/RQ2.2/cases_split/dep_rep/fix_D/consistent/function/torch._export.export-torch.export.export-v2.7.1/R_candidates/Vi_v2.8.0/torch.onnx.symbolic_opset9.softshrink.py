@_onnx_symbolic("aten::softshrink")
@symbolic_helper.parse_args("v", "f")
def softshrink(g: jit_utils.GraphContext, self, lambd):
    scalar_type = _type_utils.JitScalarType.from_value(
        self, _type_utils.JitScalarType.FLOAT
    )
    lambd_op = g.op(
        "Constant",
        value_t=torch.tensor(lambd, dtype=scalar_type.dtype()),
    )
    gt_cond = gt(g, self, lambd_op)
    gt_out = g.op(
        "Where",
        gt_cond,
        sub(g, self, lambd_op),
        g.op(
            "Constant",
            value_t=torch.tensor(0, dtype=scalar_type.dtype()),
        ),
    )
    lt_cond = lt(g, self, neg(g, lambd_op))
    lt_out = g.op(
        "Where",
        lt_cond,
        add(g, self, lambd_op),
        g.op(
            "Constant",
            value_t=torch.tensor(0, dtype=scalar_type.dtype()),
        ),
    )
    return add(g, gt_out, lt_out)
