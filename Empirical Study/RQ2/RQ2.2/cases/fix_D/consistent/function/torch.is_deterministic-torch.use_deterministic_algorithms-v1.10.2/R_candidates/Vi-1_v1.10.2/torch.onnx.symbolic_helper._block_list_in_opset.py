def _block_list_in_opset(name):
    def symbolic_fn(*args, **kwargs):
        raise RuntimeError("ONNX export failed on {}, which is not implemented for opset {}. "
                           "Try exporting with other opset versions."
                           .format(name, _export_onnx_opset_version))
    return symbolic_fn
