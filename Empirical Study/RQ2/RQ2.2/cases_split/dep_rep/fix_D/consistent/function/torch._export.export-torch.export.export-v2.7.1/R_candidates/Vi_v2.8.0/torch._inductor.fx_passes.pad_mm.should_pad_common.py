def should_pad_common(
    mat1: Tensor, mat2: Tensor, input: Optional[Tensor] = None
) -> bool:
    # It's fine we have symbolic shapes or strides as long as they
    # have hints. Later, we will make sure we only pad non-symbolic dimensions.
    def valid_shape_and_stride(t: Optional[Tensor]) -> bool:
        if t is None:
            return True

        symbolic_cnt = 0
        for x in t.size():
            if isinstance(x, int):
                continue
            elif utils.is_symbolic(x):
                if not x.node.has_hint():
                    return False
                symbolic_cnt += 1
            else:
                return False
        # filter out cases where all dimensions are symbolic
        if symbolic_cnt == len(t.size()):
            return False
        return all(
            isinstance(x, int) or (utils.is_symbolic(x) and x.node.has_hint())
            for x in t.stride()
        )

    return (
        torch._inductor.config.shape_padding
        and check_device(mat1, mat2)
        and check_dtype(mat1, mat2)
        and all(valid_shape_and_stride(t) for t in (mat1, mat2, input))
    )
