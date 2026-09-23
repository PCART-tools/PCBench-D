@register_lowering(aten._scaled_mm.default, type_promotion_kind=None)  # type: ignore[misc]
def tuned_scaled_mm(
    mat_a,
    mat_b,
    scale_a,
    scale_b,
    bias=None,
    scale_result=None,
    out_dtype=None,
    use_fast_accum=False,
    layout=None,
):
    """
    Performs an optimized matrix multiplication where scaling factors are applied
    to the inputs and/or output.

    Args:
        mat1 (Tensor): First input matrix
        mat2 (Tensor): Second input matrix
        scale1 (Tensor): Scale factor applied to mat1 (supports broadcasting)
        scale2 (Tensor): Scale factor applied to mat2 (supports broadcasting)
        bias (Tensor, optional): Optional bias tensor to add to the result
        layout: Layout hint for optimization

    Returns:
        Tensor: The result of the scaled matrix multiplication
    """
    m, n, k, layout, mat_a, mat_b = mm_args(
        mat_a, mat_b, layout=layout, out_dtype=out_dtype
    )
    # below is for getting an overview logging info of inductor mms
    counters["aten_mm_info"][f"aten._scaled_mm.default_{m}_{n}_{k}"] += 1
    log.info(
        "Tuned aten._scaled_mm.default: m=%s, n=%s, k=%s, mat1_dtype=%s, mat2_dtype=%s, output_layout=%s",
        m,
        n,
        k,
        mat_a.get_dtype(),
        mat_b.get_dtype(),
        layout,
    )

    device_type = ir.get_device_type(mat_a)
    check_supported_striding(mat_a, mat_b)

    scale_a_real, scale_b_real = realize_inputs(scale_a, scale_b)

    input_nodes: tuple[Any, ...]

    if not bias:
        input_nodes = (mat_a, mat_b, scale_a_real, scale_b_real)
    else:
        bias_real = realize_inputs(bias)
        input_nodes = (mat_a, mat_b, scale_a_real, scale_b_real, bias_real)

    aten_choice = aten__fp8_mm.bind(
        input_nodes, layout, out_dtype=out_dtype, use_fast_accum=use_fast_accum
    )

    choices = []
    if use_aten_gemm_kernels():
        choices.append(aten_choice)

    # We dont have triton lowerings for the MX variants yet
    if scale_a.dtype != torch.float32:
        return autotune_select_algorithm("scaled_mm", choices, input_nodes, layout)

    _, is_nonzero = _is_static_problem(layout)

    scaled_mm_configs = V.choices.get_scaled_mm_configs(device_type)
    scaled_persistent_mm_configs = V.choices.get_scaled_persistent_mm_configs(
        device_type
    )

    if is_nonzero and use_triton_template(layout, enable_float8=True):
        triton_input_nodes: tuple[Any, ...]
        if bias and len(mat_b.get_size()) == len(bias.get_size()) + 1:
            # Need to unsqueeze bias from [N] -> [1, N]
            triton_bias = L[aten.unsqueeze](bias, 0)
        else:
            triton_bias = bias

        if len(scale_a.get_size()) == 0 or len(scale_b.get_size()) == 0:
            assert len(scale_a.get_size()) == len(scale_b.get_size())
            # Need to unsqueeze scale from [] -> [1, 1]
            triton_scale_a = L[aten.unsqueeze](L[aten.unsqueeze](scale_a, 0), 1)
            triton_scale_b = L[aten.unsqueeze](L[aten.unsqueeze](scale_b, 0), 1)
        else:
            triton_scale_a = scale_a
            triton_scale_b = scale_b

        if bias:
            triton_input_nodes = (
                mat_a,
                mat_b,
                triton_scale_a,
                triton_scale_b,
                triton_bias,
            )
            suffix_args = 3
        else:
            triton_input_nodes = (mat_a, mat_b, triton_scale_a, triton_scale_b)
            suffix_args = 2

        # TODO (paulzhan): There is no template that exists for bias and TMA
        # Don't run tma template currently if bias exists
        if use_triton_tma_template(mat_a, mat_b) and not bias:
            for config in scaled_persistent_mm_configs(m, n, k):
                kwargs = scaled_mm_options(
                    config,
                    m,
                    n,
                    k,
                    layout,
                    scale_a,
                    scale_b,
                    use_fast_accum,
                    device_tma=True,
                )
                scaled_mm_device_tma_template.maybe_append_choice(
                    choices,
                    input_nodes=triton_input_nodes,
                    layout=layout,
                    workspace_arg=get_tma_workspace_arg(
                        num_tma_descriptors=2,
                        device=mat_a.get_device(),
                    ),
                    **kwargs,
                )

        for config in scaled_mm_configs(m, n, k):
            if V.graph.sizevars.guard_or_false(sympy.Le(k, 16)):
                # Triton crashes however uncommon for real workloads
                continue

            # On NVIDIA B200 GPUs, K dim must be >= 32 for tcgen05.mma.kind::f8f6f4.* PTX instruction to be valid
            # source: https://docs.nvidia.com/cuda/parallel-thread-execution/#tcgen05-matrix-shape
            if using_b200() and V.graph.sizevars.guard_or_false(sympy.Lt(k, 32)):
                continue

            kwargs = scaled_mm_options(
                config, m, n, k, layout, scale_a, scale_b, use_fast_accum
            )
            # possibly appends a TritonTemplateCaller to choices
            mm_template.maybe_append_choice(
                choices,
                input_nodes=triton_input_nodes,
                layout=layout,
                **kwargs,
                suffix_args=suffix_args,
                epilogue_fn=scale_mm_epilogue(),
                epilogue_fn_hash="scale_mm_epilogue",
            )

    if (
        is_nonzero
        and use_cutlass_template(layout, m, n, k)
        and _use_cutlass_for_op("scaled_mm")
    ):
        CUTLASS3xGemmTemplate.add_cutlass_gemm_choices(
            choices,
            layout,
            input_nodes,  # type: ignore[arg-type]
            use_fast_accum=use_fast_accum,  # type: ignore[arg-type]
        )

    if is_nonzero and use_ck_gemm_template(layout, m, n, k):
        CKGemmTemplate.add_ck_gemm_choices(choices, layout, input_nodes)

    return autotune_select_algorithm("scaled_mm", choices, input_nodes, layout)
