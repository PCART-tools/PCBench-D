def is_registered_op(opname, domain, version):
    if domain is None or version is None:
        warnings.warn("ONNX export failed. The ONNX domain and/or version are None.")
    global _registry
    return (domain, version) in _registry and opname in _registry[(domain, version)]
