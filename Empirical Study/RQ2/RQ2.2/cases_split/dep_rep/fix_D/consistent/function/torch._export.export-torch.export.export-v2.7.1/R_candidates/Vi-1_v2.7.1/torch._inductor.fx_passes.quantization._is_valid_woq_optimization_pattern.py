def _is_valid_woq_optimization_pattern():
    def fn(match):
        assert all(k in match.kwargs for k in ("x", "weight", "scales"))
        if not all(
            hasattr(match.kwargs[key], "meta") for key in ["x", "weight", "scales"]
        ):
            return False
        x = match.kwargs["x"].meta["val"]
        weight = match.kwargs["weight"].meta["val"]
        scales = match.kwargs["scales"].meta["val"]
        return (
            # For now, we only support woq mm kernels
            # with x.type=bfloat16 and w.type=int8
            x.dtype == torch.bfloat16
            and weight.dtype == torch.int8
            and scales.dtype == torch.bfloat16
            # _weight_int8pack_mm kernel only supports cpu now
            # TODO: add cuda kernel support instead of calling mul+sum
            and x.device.type == "cpu"
            and x.device == weight.device
            and x.device == scales.device
        )

    return fn
