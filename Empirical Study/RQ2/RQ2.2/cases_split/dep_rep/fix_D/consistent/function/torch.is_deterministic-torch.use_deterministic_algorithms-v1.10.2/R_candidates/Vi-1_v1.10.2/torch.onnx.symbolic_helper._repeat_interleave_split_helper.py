def _repeat_interleave_split_helper(g, self, reps, dim):
    if _export_onnx_opset_version <= 12:
        return g.op("Split", self, split_i=[1] * reps, axis_i=dim, outputs=reps)
    else:
        from torch.onnx.symbolic_opset13 import split
        repeats = g.op("Constant", value_t=torch.tensor([1] * reps))
        return split(g, self, repeats, dim, _outputs=reps)
