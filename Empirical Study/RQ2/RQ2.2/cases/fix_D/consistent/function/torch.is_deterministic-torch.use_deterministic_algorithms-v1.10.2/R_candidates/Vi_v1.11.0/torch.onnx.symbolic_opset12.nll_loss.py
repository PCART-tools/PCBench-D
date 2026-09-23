def nll_loss(g, self, target, weight, reduction, ignore_index):
    # none reduction : onnx::Constant[value={0}]
    # mean reduction : onnx::Constant[value={1}]
    # sum reduction : onnx::Constant[value={2}]
    reduction = sym_help._maybe_get_const(reduction, "i")
    reduction_vals = ["none", "mean", "sum"]
    reduction = reduction_vals[reduction]

    # in onnx NegativeLogLikelihoodLoss specification, ignore_index is optional without default value.
    # therefore we need to set ignore_index attribute even if it is not specified (e.g. ignore_index=-100).
    ignore_index = sym_help._maybe_get_const(ignore_index, "i")
    if weight.node().mustBeNone():
        nllloss = g.op("NegativeLogLikelihoodLoss", self, target, reduction_s=reduction, ignore_index_i=ignore_index)
    else:
        nllloss = g.op("NegativeLogLikelihoodLoss", self, target, weight, reduction_s=reduction, ignore_index_i=ignore_index)

    return nllloss
