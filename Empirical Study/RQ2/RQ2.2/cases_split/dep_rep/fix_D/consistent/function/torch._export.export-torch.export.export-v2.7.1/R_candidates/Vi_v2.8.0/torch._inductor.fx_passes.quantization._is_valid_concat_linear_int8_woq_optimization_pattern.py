def _is_valid_concat_linear_int8_woq_optimization_pattern():
    def fn(match):
        if not config.cpp.enable_concat_linear:
            return False
        assert all(k in match.kwargs for k in ("x", "w1", "w2", "w3", "scales"))
        if not all(
            hasattr(match.kwargs[key], "meta")
            for key in ["x", "w1", "w2", "w3", "scales"]
        ):
            return False
        x = match.kwargs["x"].meta["val"]
        w1 = match.kwargs["w1"].meta["val"]
        w2 = match.kwargs["w2"].meta["val"]
        w3 = match.kwargs["w3"].meta["val"]
        scales = match.kwargs["scales"].meta["val"]
        if len(match.kwargs["scales"].meta["val"].size()) > 1:
            return False
        num_scales = match.kwargs["scales"].meta["val"].numel()
        w1_cols = match.kwargs["w1"].meta["val"].size()[0]
        w2_cols = match.kwargs["w2"].meta["val"].size()[0]
        w3_cols = match.kwargs["w3"].meta["val"].size()[0]
        # Technically, the shapes of the three weights need not be equal.
        # But currently, we only enable replacement in this case.
        if w1_cols != w2_cols or w2_cols != w3_cols:
            return False
        if 3 * w1_cols != num_scales:
            return False
        return (
            # For now, we only support woq mm kernels
            # with x.type=bfloat16 and w.type=int8
            x.dtype == torch.bfloat16
            and w1.dtype == torch.int8
            and w2.dtype == torch.int8
            and w3.dtype == torch.int8
            and scales.dtype == torch.bfloat16
            # _weight_int8pack_mm kernel only supports cpu now
            # TODO: add cuda kernel support instead of calling mul+sum
            and x.device.type == "cpu"
            and x.device == w1.device
            and w1.device == w2.device
            and w2.device == w3.device
            and x.device == scales.device
        )

    return fn
