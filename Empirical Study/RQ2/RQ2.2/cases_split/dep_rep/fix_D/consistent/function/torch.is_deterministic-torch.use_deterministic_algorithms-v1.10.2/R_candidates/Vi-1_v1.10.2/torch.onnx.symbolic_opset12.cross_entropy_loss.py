def cross_entropy_loss(g, self, target, weight, reduction, ignore_index, label_smoothing):
    # none reduction : onnx::Constant[value={0}]
    # mean reduction : onnx::Constant[value={1}]
    # sum reduction : onnx::Constant[value={2}]
    reduction = sym_help._maybe_get_const(reduction, "i")
    reduction_vals = ["none", "mean", "sum"]
    reduction = reduction_vals[reduction]

    label_smoothing = sym_help._maybe_get_const(label_smoothing, "f")
    if label_smoothing > 0.0:
        raise RuntimeError("Unsupported: ONNX does not support label_smoothing")

    # in onnx SoftmaxCrossEntropyLoss specification, ignore_index is optional without default value.
    # therefore we need to set ignore_index attribute even if it is not specified (e.g. ignore_index=-100).
    ignore_index = sym_help._maybe_get_const(ignore_index, "i")
    if weight.node().mustBeNone():
        celoss = g.op("SoftmaxCrossEntropyLoss", self, target, reduction_s=reduction, ignore_index_i=ignore_index)
    else:
        celoss = g.op("SoftmaxCrossEntropyLoss", self, target, weight, reduction_s=reduction, ignore_index_i=ignore_index)

    return celoss
