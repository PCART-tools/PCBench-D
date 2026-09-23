def sdpa_constraint(fx_node, *args, **kwargs):
    # sdpa requires dense last dimension]

    def apply_constraint(idx, arg, fx_arg):
        if not isinstance(arg, ir.IRNode):
            return arg

        meta_val = fx_arg.meta["val"]
        meta_stride_expr = [
            s.node.expr if isinstance(s, torch.SymInt) else s for s in meta_val.stride()
        ]

        stride_order = ir.get_stride_order(meta_val.stride())

        if stride_order and stride_order[-1] != 0:
            # contiguous stride order
            stride_order = list(reversed(range(len(arg.get_size()))))

        if (
            fx_node.target
            == aten._scaled_dot_product_efficient_attention_backward.default
            and idx in (0, 5)
        ):
            assert len(stride_order) == 4
            # The 0 and 5th arguments for aten._scaled_dot_product_efficient_attention_backward.default
            # are for out and gradient_out. They have to be in
            # (3, 1, 2, 0) stride order. Otherwise the kernel will crash.
            # Check https://github.com/pytorch/pytorch/issues/138772
            stride_order = (3, 1, 2, 0)

        if not meta_val.is_cuda:
            return ir.ExternKernel.require_stride_order(arg, stride_order)

        # This is the minimum alignment required by SDPA kernels for attention_bias.
        # This value can be found in pytorch/aten/src/ATen/native/transformers/attention.cpp preprocess_mask
        ALIGNMENT = 8

        # effn_attn_fwd does requires dense last dim, not just alignment
        effn_attn_fwd_bias = (
            fx_node.target
            == torch.ops.aten._scaled_dot_product_efficient_attention.default
            and idx == 3
        )

        assert isinstance(arg, TensorBox)
        if len(arg.get_size()) not in (3, 4):
            return arg

        if ir.is_aligned_realized_tensor(arg, ALIGNMENT):
            return ir.try_match_insignificant_strides(
                ir.ExternKernel.realize_input(arg), meta_stride_expr
            )

        if (
            isinstance(arg, IRNode)
            and arg.maybe_get_stride() is not None
            and ir.is_aligned_realized_tensor(arg, ALIGNMENT)
        ):
            return ir.try_match_insignificant_strides(
                ir.ExternKernel.realize_input(arg), meta_stride_expr
            )

        if effn_attn_fwd_bias:
            out_size = list(arg.get_size())

            expanded_dims = []
            # We require a dense last dimension, but the other strides
            # can be expanded, which results in a smaller tensor
            maybe_stride = arg.maybe_get_stride()
            for i in range(len(arg.get_size()) - 1):
                if V.graph.sizevars.statically_known_equals(meta_stride_expr[i], 0) or (
                    maybe_stride is not None
                    and V.graph.sizevars.statically_known_equals(maybe_stride[i], 0)
                ):
                    expanded_dims.append(i)

            # Now, pad strides to alignment
            out_strides = [-1] * len(out_size)
            out_strides[-1] = 1
            stride = 1
            for i in range(len(out_size) - 2, -1, -1):
                if out_strides[i + 1] != 0:
                    stride = stride * out_size[i + 1]

                # the expanded dims still need to be aligned, if they are,
                # we can make them expanded by setting the stride equal to 0
                if i in expanded_dims:
                    if V.graph.sizevars.statically_known_equals(
                        out_strides[i + 1] % ALIGNMENT, 0
                    ):
                        out_strides[i] = 0
                        continue

                if not V.graph.sizevars.statically_known_equals(stride % ALIGNMENT, 0):
                    stride = ceildiv(stride, ALIGNMENT) * ALIGNMENT

                out_strides[i] = stride

            return ir.ExternKernel.require_exact_strides(arg, out_strides)

        if ir.is_aligned_realized_tensor(arg, ALIGNMENT):
            return ir.try_match_insignificant_strides(
                ir.ExternKernel.realize_input(arg), meta_stride_expr
            )

        if (
            isinstance(arg, IRNode)
            and arg.maybe_get_stride() is not None
            and ir.is_aligned_realized_tensor(arg, ALIGNMENT)
        ):
            return ir.try_match_insignificant_strides(
                ir.ExternKernel.realize_input(arg), meta_stride_expr
            )

        def is_aligned(x):
            return (V.graph.sizevars.size_hint(x.get_size()[-1]) % ALIGNMENT) == 0

        if isinstance(arg.data, ir.BaseView):
            if not is_aligned(arg):
                if is_aligned(arg.unwrap_view()):
                    return ir.try_match_insignificant_strides(
                        ir.ExternKernel.realize_input(arg), meta_stride_expr
                    )

        return ir.ExternKernel.require_stride_order(arg, stride_order)

    args = tuple(
        apply_constraint(idx, arg, fx_arg)
        for idx, (arg, fx_arg) in enumerate(zip(args, fx_node.args))
    )
    kwargs = {k: apply_constraint(-1, v, fx_node.kwargs[k]) for k, v in kwargs.items()}
    return args, kwargs
