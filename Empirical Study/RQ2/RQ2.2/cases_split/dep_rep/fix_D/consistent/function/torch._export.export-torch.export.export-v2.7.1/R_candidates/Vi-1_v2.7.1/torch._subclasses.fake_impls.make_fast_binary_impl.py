def make_fast_binary_impl(slow_ref):
    def fast_binary_impl(mode, *args, **kwargs):
        def slow(msg):
            count_label(f"slow {msg}")
            with mode:
                return slow_ref(*args, **kwargs)

        count_label("attempt fast")

        # Fast path (based off of TensorIterator fast path).
        # Unfortunately, there is no way to easily deduplicate
        # this with either the TensorIterator C++ implementation
        # (which we don't want to SymIntify, and also the algorithm
        # here is slightly different from TensorIterator to allow
        # for broadcasting), nor the PrimTorch implementation
        # (which does not actually implement a fast path.)

        operands = args

        # compute_shape
        final_shape = None
        for op in operands:
            shape = op.shape if isinstance(op, torch.Tensor) else ()
            if final_shape is None:
                final_shape = shape
            # TODO: Minor optimization: track if the shapes
            # were equal so you can skip the equality check
            # below if unnecessary
            final_shape = infer_size(final_shape, shape)
        assert final_shape is not None

        from torch.fx.experimental.symbolic_shapes import guard_size_oblivious, sym_eq

        # Do some extra safety checks to see if the output
        # stride is obvious
        for op in operands:
            if (
                isinstance(op, torch.Tensor)
                and len(op.shape) == len(final_shape)
                and guard_size_oblivious(sym_eq(op.shape, final_shape))
            ):
                break
        else:
            return slow("both tensors nontrivially broadcast")

        # compute_types
        cpu = torch.device("cpu")
        common_device = cpu
        common_dtype = None
        has_different_input_dtypes = False
        for op in operands:
            if not isinstance(op, torch.Tensor):
                # Use elementwise_dtypes for the tricky case
                has_different_input_dtypes = True
                continue
            if common_device == cpu and not op.device.type == "cpu":
                common_device = op.device
            # Slightly simplified here as target_dtype cannot vary
            if common_dtype is None:
                common_dtype = op.dtype
            elif common_dtype != op.dtype:
                has_different_input_dtypes = True

        if has_different_input_dtypes:
            # compute promotion
            # TODO: we don't need the compute type
            _, common_dtype = elementwise_dtypes(
                *operands, type_promotion_kind=ELEMENTWISE_TYPE_PROMOTION_KIND.DEFAULT
            )

        # check all tensors on same device
        # cpu scalars are assumed allow
        current_cpu_scalars_on_non_cpu = 0
        max_cpu_scalars_on_non_cpu = 1  # hard coded atm
        for op in operands:
            if not isinstance(op, torch.Tensor):
                continue
            if common_device != cpu and op.dim() == 0 and op.device == cpu:
                if current_cpu_scalars_on_non_cpu >= max_cpu_scalars_on_non_cpu:
                    return slow("error")
                current_cpu_scalars_on_non_cpu += 1
            elif op.device != common_device:
                return slow("error")

        # compute_fast_setup_type
        is_contiguous = True
        is_channels_last = True
        # TODO: is_non-overlapping_and_dense (not bound from Python
        # no inplace, no out, everything defined

        if is_noncontiguous_supported(common_device):
            for op in operands:
                if not isinstance(op, torch.Tensor):
                    continue
                is_contiguous = is_contiguous and op.is_contiguous(
                    memory_format=torch.contiguous_format
                )
                is_channels_last = is_channels_last and op.is_contiguous(
                    memory_format=torch.channels_last
                )
        if is_contiguous:
            # do contiguous
            count_label("fast is_contiguous")
            return FakeTensor(
                mode,
                torch.empty(
                    final_shape,
                    dtype=common_dtype,
                    device="meta",
                    memory_format=torch.contiguous_format,
                ),
                device=common_device,
            )
        if is_channels_last:
            count_label("fast channels_last")
            # do channels last
            return FakeTensor(
                mode,
                torch.empty(
                    final_shape,
                    dtype=common_dtype,
                    device="meta",
                    memory_format=torch.channels_last,
                ),
                device=common_device,
            )

        return slow("no contiguity match")

    return fast_binary_impl
