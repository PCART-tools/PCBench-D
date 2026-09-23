def mobilenetv2_spec():
    return {
        "forward": CompileSpec(
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
    }
