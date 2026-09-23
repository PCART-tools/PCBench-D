def CompileSpec(*args, **kwargs):
    """
    CompileSpec specifies the model information.
    Example:
    cs = CompileSpec(
            inputs=(
                TensorSpec(
                    shape=[1, 3, 224, 224],
                ),
            ),
            outputs=(
                TensorSpec(
                    shape=[1, 1000],
                ),
            ),
            backend=CoreMLComputeUnit.CPU,
            allow_low_precision=True,
    ),
    """
    return astuple(_CompileSpec(*args, **kwargs))
