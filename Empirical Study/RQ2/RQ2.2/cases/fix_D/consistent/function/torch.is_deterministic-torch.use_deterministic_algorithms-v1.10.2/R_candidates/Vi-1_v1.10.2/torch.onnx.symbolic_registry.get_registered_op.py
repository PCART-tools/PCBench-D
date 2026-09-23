def get_registered_op(opname, domain, version):
    if domain is None or version is None:
        warnings.warn("ONNX export failed. The ONNX domain and/or version are None.")
    global _registry
    if not is_registered_op(opname, domain, version):
        msg = "Exporting the operator " + opname + " to ONNX opset version " + str(version) + " is not supported. "
        supported_version = get_op_supported_version(opname, domain, version)
        if supported_version is not None:
            msg += "Support for this operator was added in version " + str(supported_version) + ", try exporting with this version."
        else:
            msg += "Please feel free to request support or submit a pull request on PyTorch GitHub."
        raise RuntimeError(msg)
    return _registry[(domain, version)][opname]
