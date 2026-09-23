def get_op_supported_version(opname, domain, version):
    iter_version = version
    while iter_version <= _onnx_main_opset:
        ops = [op[0] for op in get_ops_in_version(iter_version)]
        if opname in ops:
            return iter_version
        iter_version += 1
    return None
