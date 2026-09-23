def skipIfNotRegistered(op_name, message):
    """Wraps the decorator to hide the import of the `core`.

    Args:
        op_name: Check if this op is registered in `core._REGISTERED_OPERATORS`.
        message: message to fail with.

    Usage:
        @skipIfNotRegistered('MyOp', 'MyOp is not linked!')
            This will check if 'MyOp' is in the caffe2.python.core
    """
    try:
        from caffe2.python import core
        skipper = unittest.skipIf(op_name not in core._REGISTERED_OPERATORS,
                                  message)
    except ImportError:
        skipper = unittest.skip("Cannot import `caffe2.python.core`")
    return skipper
