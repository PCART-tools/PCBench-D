@_onnx_symbolic("aten::hardshrink")
@symbolic_helper.parse_args("v", "f")
def hardshrink(g: jit_utils.GraphContext, self, lambd):
    scalar_type = _type_utils.JitScalarType.from_value(
        self, _type_utils.JitScalarType.FLOAT
    )
    lambd_op = g.op(
        "Constant",
        value_t=torch.tensor(lambd, dtype=scalar_type.dtype()),
    )
    cond = logical_or(g, gt(g, self, lambd_op), lt(g, self, neg(g, lambd_op)))
    return g.op(
        "Where",
        cond,
        self,
        g.op(
            "Constant",
            value_t=torch.tensor(0, dtype=scalar_type.dtype()),
        ),
    )
