@_onnx_symbolic("aten::cross")
@symbolic_helper.parse_args("v", "v", "i")
def cross(g: jit_utils.GraphContext, input, other, dim=None):
    dim = symbolic_helper._get_dim_for_cross(input, dim)
    # If we have two tensors such that
    # A = [a, b, c], B = [d, e, f], we permute the tensor such that we have
    # After first roll,
    # A' = [b, c, a], B' = [f, d, e], so that we calculate (b*f, c*d, a*e)
    roll_x_1 = roll(g, input, [2], [dim])
    roll_y_1 = roll(g, other, [1], [dim])
    # After second roll,
    # A' = [c, a, b], B' = [e, f, d], so that we calculate (c*e, a*f, b*d)
    roll_x_2 = roll(g, input, [1], [dim])
    roll_y_2 = roll(g, other, [2], [dim])
    # cross product is calculated as
    # result = [(b*f - c*e), (c*d - a*f), (a*e - b*d)]
    return sub(g, mul(g, roll_x_1, roll_y_1), mul(g, roll_x_2, roll_y_2))
