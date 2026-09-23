@_onnx_symbolic("aten::lerp")
def lerp(g: jit_utils.GraphContext, self, end, weight):
    # Conditional for better numeric. This has been discussed in
    # https://github.com/pytorch/pytorch/pull/18871
    diff = g.op("Sub", end, self)
    return where(
        g,
        g.op("Less", weight, g.op("Constant", value_t=torch.tensor(0.5))),
        g.op("Add", self, g.op("Mul", weight, diff)),
        g.op(
            "Sub",
            end,
            g.op(
                "Mul",
                diff,
                g.op("Sub", g.op("Constant", value_t=torch.tensor(1.0)), weight),
            ),
        ),
    )
