@_onnx_symbolic("aten::bucketize")
@symbolic_helper.parse_args("v", "v", "b", "b")
def bucketize(
    g: jit_utils.GraphContext, self, boundaries, out_int32=False, right=False
):
    out_type = _C_onnx.TensorProtoDataType.INT64
    if out_int32:
        out_type = _C_onnx.TensorProtoDataType.INT32
    # A tensor expanded_boundaries is created such that it
    # contains a copy of boundaries for each element of self.
    new_shape = g.op("Concat", g.op("Shape", boundaries), g.op("Shape", self), axis_i=0)
    # Unsqueeze step is performed to respect ONNX's numpy style broadcasting for comparison ops
    # https://github.com/onnx/onnx/blob/main/docs/Broadcasting.md
    tensor_rank = symbolic_helper._get_tensor_rank(self)
    assert tensor_rank is not None
    unsqueeze_axes = list(range(1, tensor_rank + 1))
    expanded_boundaries = expand(
        g,
        symbolic_helper._unsqueeze_helper(g, boundaries, unsqueeze_axes),
        new_shape,
        None,
    )
    # Compare each element of self to boundaries to get a tensor
    # with leading 1s and trailing 0s.
    # e.g., 4 > [1, 3, 4] = [1, 1, 0]
    # The index of the last 1 is the bucket where the element should go.
    if right:
        cond = ge(g, self, expanded_boundaries)
    else:
        cond = gt(g, self, expanded_boundaries)
    cond_out = g.op("Cast", cond, to_i=out_type)
    # Sum to get the number of 1s corresponding to each element,
    # which is the same as the bucket index.
    # e.g., sum(4 > [1, 3, 4]) = sum([1, 1, 0]) = 2
    return symbolic_helper._reducesum_helper(g, cond_out, axes_i=[0], keepdims_i=0)
