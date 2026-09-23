def _index_fill_reshape_helper(g, self, dim, index):
    # 1. reshape index => [1, ..., 1, dim, 1, ..., 1]
    # 2. expand index => [..., dim, ...], same shape as self except for dim.
    # 3. expand value as well.
    # 4. apply onnx::scatter.

    from torch.onnx.symbolic_opset9 import expand
    if _export_onnx_opset_version <= 10:
        from torch.onnx.symbolic_opset9 import scatter
    else:
        # for mypy, scatter was imported two lines above
        from torch.onnx.symbolic_opset11 import scatter  # type: ignore[no-redef]

    if self.type().dim() is None:
        return _unimplemented("index_fill", "input rank not accesible")
    self_dim = self.type().dim()
    dim_value = _parse_arg(dim, "i")
    unsqueezed_index = _unsqueeze_helper(g, index, [i for i in range(self_dim) if i != dim_value])
    expanded_index_shape = scatter(g, g.op("Shape", self), 0,
                                   _unsqueeze_helper(g, dim, [0]), g.op("Shape", index))
    expanded_index = expand(g, unsqueezed_index, expanded_index_shape, None)
    return expanded_index_shape, expanded_index
