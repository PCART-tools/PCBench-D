@register_lowering(aten._scaled_mm.default, type_promotion_kind=None)  # type: ignore[misc]
def tuned_scaled_mm(
    mat_a: TensorBox,
    mat_b: TensorBox,
    scale_a: TensorBox,
    scale_b: TensorBox,
    bias: Optional[TensorBox] = None,
    scale_result: Optional[TensorBox] = None,
    out_dtype: Optional[torch.dtype] = None,
    use_fast_accum: bool = False,
    layout: Optional[Layout] = None,
) -> TensorBox:
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

    check_supported_striding(mat_a, mat_b)

    scale_a, scale_b = realize_inputs(scale_a, scale_b)

    input_nodes: tuple[Any, ...]
    # workaround for Inductor not supporting optional tensor input arguments
    if bias is None:
        input_nodes = (mat_a, mat_b, scale_a, scale_b)
        triton_template = scaled_mm_template
    else:
        bias = realize_inputs(bias)
        input_nodes = (mat_a, mat_b, scale_a, scale_b, bias)
        triton_template = scaled_mm_bias_template

    aten_choice = aten__fp8_mm.bind(
        input_nodes, layout, out_dtype=out_dtype, use_fast_accum=use_fast_accum
    )

    choices: list[ChoiceCaller] = []
    if use_aten_gemm_kernels():
        choices.append(aten_choice)

    _, is_nonzero = _is_static_problem(layout)

    if is_nonzero and use_triton_template(layout, enable_float8=True):
        if use_persistent_tma(k, bias is not None):
            for config in scaled_persistent_mm_configs(m, n, k):
                kwargs = scaled_mm_options_device_tma(
                    config, m, n, k, layout, scale_a, scale_b, use_fast_accum
                )
                input_nodes = (mat_a, mat_b, scale_a, scale_b)
                scaled_mm_device_tma_template.maybe_append_choice(
                    choices,
                    input_nodes=input_nodes,
                    layout=layout,
                    workspace_arg=get_tma_workspace_arg(
                        num_tma_descriptors=2,
                        device=mat_a.get_device(),
                    ),
                    **kwargs,
                )
        else:
            for config in scaled_mm_configs(m, n, k):
                if k == 16 and config.kwargs["BLOCK_M"] >= 64:
                    continue  # Triton crashes in this case

                # On NVIDIA B200 GPUs, K dim must be >= 32 for tcgen05.mma.kind::f8f6f4.* PTX instruction to be valid
                # source: https://docs.nvidia.com/cuda/parallel-thread-execution/#tcgen05-matrix-shape
                if using_b200() and k < 32:
                    continue

                kwargs = scaled_mm_options(
                    config, m, n, k, layout, scale_a, scale_b, use_fast_accum
                )
                # possibly appends a TritonTemplateCaller to choices
                triton_template.maybe_append_choice(
                    choices,
                    input_nodes=input_nodes,
                    layout=layout,
                    **kwargs,
                )

    if is_nonzero and use_ck_gemm_template(layout, m, n, k):
        CKGemmTemplate.add_ck_gemm_choices(choices, layout, input_nodes)

    if should_fallback_to_aten(choices):
        return aten_choice.output_node()

    return autotune_select_algorithm("scaled_mm", choices, input_nodes, layout)
