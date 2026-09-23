    def mps_ops_error_inputs_modifier(ops: Sequence[OpInfo]) -> Sequence[OpInfo]:
        # Error input samples do not take a dtype argument.
        XFAILLIST = {
            # Exceptions are not raised
            "__rmod__",
            "__rsub__",
            "__rpow__",
            "bernoulli",
            "clamp_max",
            "clamp_min",
            "masked_scatter",
            # unsupported float64 dtype
            "cat",
            "complex",
            "multinomial",
            "nn.functional.conv1d",
            "nn.functional.conv2d",
            "nn.functional.conv3d",
            "gather",
            "scatter",
            "scatter_add",
            # MPS does not support tensor dimensions > 16
            "amax",
            "amin",
            "aminmax",
            # memory overlapping checks
            "index_select",
            # unimplemented
            "logcumsumexp",
        }

        def addDecorator(op: OpInfo, d: DecorateInfo) -> None:
            op.decorators = op.decorators + (d,)

        for op in ops:
            key = op.name + op.variant_test_name
            if key in XFAILLIST:
                addDecorator(op, DecorateInfo(unittest.expectedFailure))

        return ops
