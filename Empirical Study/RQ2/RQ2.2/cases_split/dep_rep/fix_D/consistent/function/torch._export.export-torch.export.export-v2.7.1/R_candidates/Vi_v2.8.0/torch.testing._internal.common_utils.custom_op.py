@contextmanager
def custom_op(opname, symbolic_fn, opset_version):
    """Context manager/decorator to test ONNX export with custom operator"""
    try:
        register_custom_op_symbolic(opname, symbolic_fn, opset_version)
        yield
    finally:
        unregister_custom_op_symbolic(opname, opset_version)
