@register_lowering(aten.mm, type_promotion_kind=None)
def tuned_mm(mat1, mat2, *, layout=None):
    m, n, k, layout, mat1, mat2 = mm_args(mat1, mat2, layout=layout)
    name = "mm"

    # below is for getting an overview logging info of inductor mms
    counters["aten_mm_info"][f"aten.mm_{m}_{n}_{k}"] += 1
    log.info(
        "Tuned aten.mm: m=%s, n=%s, k=%s, mat1_dtype=%s, mat2_dtype=%s, output_layout=%s",
        m,
        n,
        k,
        mat1.get_dtype(),
        mat2.get_dtype(),
        layout,
    )

    aten_layout = layout
    if not use_max_autotune():
        aten_layout = FlexibleLayout(
            device=layout.device, dtype=layout.dtype, size=layout.size
        )

    # options to tune from
    choices = (
        [aten_mm.bind((mat1, mat2), aten_layout)] if use_aten_gemm_kernels() else []
    )
    static_shape, is_nonzero = _is_static_problem(layout)
    if is_nonzero and use_triton_template(layout):
        for config in mm_configs(m, n, k, **mm_config_kwargs(ir.get_device_type(mat1))):
            mm_template.maybe_append_choice(
                choices,
                input_nodes=(mat1, mat2),
                layout=layout,
                **mm_options(config, m, n, k, layout),
            )
        if use_triton_tma_template(mat1, mat2):
            for config in persistent_mm_configs(
                m, n, k, **mm_config_kwargs(ir.get_device_type(mat1))
            ):
                persistent_tma_mm_template.maybe_append_choice(
                    choices,
                    input_nodes=(mat1, mat2),
                    layout=layout,
                    workspace_arg=get_tma_workspace_arg(
                        num_tma_descriptors=2,
                        device=mat1.get_device(),
                    ),
                    **mm_options(config, m, n, k, layout),
                    **persistent_mm_options(mat1, mat2),
                )

    if is_nonzero and use_cutlass_template(layout, m, n, k):
        CUTLASS3xGemmTemplate.add_cutlass_gemm_choices(choices, layout, [mat1, mat2])

    if is_nonzero and use_ck_gemm_template(layout, m, n, k):
        CKGemmTemplate.add_ck_gemm_choices(choices, layout, [mat1, mat2])

    if use_cpp_gemm_template(layout, mat1, mat2):
        CppGemmTemplate.add_choices(
            choices,
            layout,
            [mat1, mat2],
        )

    input_nodes = [mat1, mat2]
    if (
        is_nonzero
        and use_triton_template(layout)
        and torch._inductor.config.run_autoheuristic(name)
        and is_triton(mat1)
    ):
        always_included = []
        if use_aten_gemm_kernels():
            always_included.append("extern_mm")
        num_choices_before_extra_configs = len(choices)
        for config in extra_mm_configs(
            m, n, k, **mm_config_kwargs(ir.get_device_type(mat1))
        ):
            mm_template.maybe_append_choice(
                choices,
                input_nodes=(mat1, mat2),
                layout=layout,
                **mm_options(config, m, n, k, layout),
            )

        # using AutoHeuristic for ranking
        ah_choices = mm_autoheuristic(
            mat1,
            mat2,
            m,
            n,
            k,
            choices,
            name,
            input_nodes,
            mm_operations(),
            None,
            top_k=10,
            always_included=always_included,
        )
        if not torch._inductor.config.collect_autoheuristic(name):
            # if we are collecting data, we do not want to modify choices
            if ah_choices is not None and len(ah_choices) > 0:
                # the order in which autoheuristic returns choices is not the same as
                # as the order of choices, which affects things like epilogue fusion.
                # once epilogue fusion benchmarks choices in sorted order, I think we can
                # just use the order returned by autoheuristic
                choices = [choice for choice in choices if choice in ah_choices]
            else:
                choices = choices[:num_choices_before_extra_configs]

    for k in inductor_config.external_matmul:
        choices.append(lazy_register_extern_choice(k).bind((mat1, mat2), layout))

    if should_fallback_to_aten(choices):
        return aten_mm.bind((mat1, mat2), aten_layout).output_node()

    return autotune_select_algorithm(name, choices, [mat1, mat2], layout)
