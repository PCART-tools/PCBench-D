def register_op(opname, op, domain, version):
    if domain is None or version is None:
        warnings.warn("ONNX export failed. The ONNX domain and/or version to register are None.")
    global _registry
    if not is_registered_version(domain, version):
        _registry[(domain, version)] = {}
    _registry[(domain, version)][opname] = op
