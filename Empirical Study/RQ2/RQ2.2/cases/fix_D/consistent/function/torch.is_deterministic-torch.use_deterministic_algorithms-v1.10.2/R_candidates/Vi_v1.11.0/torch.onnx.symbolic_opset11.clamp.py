def clamp(g, self, min, max):
    dtype = self.type().scalarType()

    def _cast_if_not_none(tensor, dtype):
        if tensor is not None and not sym_help._is_none(tensor):
            return g.op("Cast", tensor, to_i=sym_help.cast_pytorch_to_onnx[dtype])
        else:
            return tensor

    if dtype is not None:
        min = _cast_if_not_none(min, dtype)
        max = _cast_if_not_none(max, dtype)

    if sym_help._is_none(min):
        return clamp_max(g, self, max)
    elif sym_help._is_none(max):
        return clamp_min(g, self, min)
    else:
        if sym_help._get_tensor_rank(min) == 0 and sym_help._get_tensor_rank(max) == 0:
            return g.op("Clip", self, min, max)
        else:
            return clamp_max(g, clamp_min(g, self, min), max)
