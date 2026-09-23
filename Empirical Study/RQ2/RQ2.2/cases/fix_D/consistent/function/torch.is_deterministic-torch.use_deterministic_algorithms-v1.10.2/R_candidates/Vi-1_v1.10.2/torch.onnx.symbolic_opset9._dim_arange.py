@parse_args("v", "i")
def _dim_arange(g, like, dim):
    like_shape = g.op("Shape", like)
    stop = g.op("Gather", like_shape, g.op("Constant", value_t=torch.tensor(dim)), axis_i=0)
    if sym_help._operator_export_type == torch.onnx.OperatorExportTypes.ONNX_ATEN_FALLBACK:
        return g.op("_caffe2::Range", stop)
    else:
        # aten::arange(Scalar end, ScalarType dtype, Layout, Device, bool pin_memory)
        return arange(g, stop, 4, None, None, None)
