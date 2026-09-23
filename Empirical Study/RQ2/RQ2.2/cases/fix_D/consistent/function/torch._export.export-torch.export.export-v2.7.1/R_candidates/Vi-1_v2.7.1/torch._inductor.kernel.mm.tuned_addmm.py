@register_lowering(aten.addmm, type_promotion_kind=None)
def tuned_addmm(inp, mat1, mat2, *, alpha=1, beta=1, layout=None):
    ordered_kwargs_for_cpp_kernel = ("beta", "alpha")
    m, n, k, layout, mat1, mat2, inp_expanded = mm_args(mat1, mat2, inp, layout=layout)
    static_shape, is_nonzero = _is_static_problem(layout)

    # below is for getting an overview logging info of inductor mms
    counters["aten_mm_info"][f"aten.addmm_{m}_{n}_{k}"] += 1
    log.info(
        "Tuned aten.addmm: m=%s, n=%s, k=%s, mat1_dtype=%s, mat2_dtype=%s, output_layout=%s",
        m,
        n,
        k,
        mat1.get_dtype(),
        mat2.get_dtype(),
        layout,
    )

    if (not is_nonzero) or (not use_max_autotune()):
        # Use a FlexibleLayout if we are not autotuning.
        # This allows padding strides for the output.
        from torch._inductor.ir import FixedLayout, FlexibleLayout

        if isinstance(layout, FixedLayout):
            layout = FlexibleLayout(
                device=layout.device, dtype=layout.dtype, size=layout.size
            )
        choices = (
            [
                aten_addmm.bind(
                    (inp, mat1, mat2),
                    layout,
                    alpha=alpha,
                    beta=beta,
                )
            ]
            if use_aten_gemm_kernels()
            else []
        )
        return autotune_select_algorithm("addmm", choices, [inp, mat1, mat2], layout)

    choices = (
        [
            aten_addmm.bind(
                (inp_expanded, mat1, mat2),
                layout,
                alpha=alpha,
                beta=beta,
            )
        ]
        if use_aten_gemm_kernels()
        else []
    )

    if (
        use_aten_gemm_kernels()
        and inp_expanded.get_stride()[0] == 0
        and inp_expanded.get_device().type == "cuda"
        and inductor_config.triton.autotune_cublasLt
    ):
        # unexpand inp to make sure fused addmm from cublasLt is used
        choices.insert(
            0,
            aten_bias_addmm.bind(
                (inp_expanded, mat1, mat2), layout, alpha=alpha, beta=beta
            ),
        )

    if is_nonzero and use_triton_template(layout):
        for config in mm_configs(m, n, k, **mm_config_kwargs(ir.get_device_type(mat1))):
            mm_template.maybe_append_choice(
                choices,
                input_nodes=(inp_expanded, mat1, mat2),
                layout=layout,
                **mm_options(config, m, n, k, layout),
                prefix_args=1,
                epilogue_fn=addmm_epilogue(layout.dtype, alpha, beta),
            )

        if use_triton_tma_template(mat1, mat2):
            for config in persistent_mm_configs(
                m, n, k, **mm_config_kwargs(ir.get_device_type(mat1))
            ):
                persistent_tma_mm_template.maybe_append_choice(
                    choices,
                    input_nodes=(inp_expanded, mat1, mat2),
                    layout=layout,
                    workspace_arg=get_tma_workspace_arg(
                        num_tma_descriptors=2,
                        device=mat1.get_device(),
                    ),
                    **mm_options(config, m, n, k, layout),
                    **persistent_mm_options(mat1, mat2),
                    prefix_args=1,
                    epilogue_fn=addmm_epilogue(layout.dtype, alpha, beta),
                )

    if static_shape and is_nonzero and use_cutlass_template(layout, m, n, k):
        # Filter out a known cause of CUDA illegal memory access errors
        # broadcasting on the last dim of the bias term seems not to be working
        # in the linear GEMM epilogue used by addmm.
        if (
            PythonWrapperCodegen.statically_known_int_or_none(
                inp_expanded.layout.stride[-1]
            )
            != 0
        ):
            CUTLASS3xGemmTemplate.add_cutlass_gemm_choices(
                choices,
                layout,
                [mat1, mat2, inp_expanded],
                alpha=alpha,
                beta=beta,
                input_reorder=[2, 0, 1],
            )

    if is_nonzero and use_ck_gemm_template(layout, m, n, k):
        CKGemmTemplate.add_ck_gemm_choices(
            choices,
            layout,
            [mat1, mat2, inp_expanded],
            alpha=alpha,
            beta=beta,
            input_reorder=[2, 0, 1],
        )

    if use_cpp_gemm_template(layout, mat1, mat2):
        CppGemmTemplate.add_choices(
            choices,
            layout,
            [inp_expanded, mat1, mat2],
            alpha=alpha,
            beta=beta,
            has_bias=True,
        )

    if should_fallback_to_aten(choices):
        choices.append(
            aten_addmm.bind(
                (inp_expanded, mat1, mat2),
                layout,
                ordered_kwargs_for_cpp_kernel,
                alpha=alpha,
                beta=beta,
            )
        )

        if (
            inp_expanded.get_stride()[0] == 0
            and inp_expanded.get_device().type == "cuda"
            and inductor_config.triton.autotune_cublasLt
        ):
            # unexpand inp to make sure fused addmm from cublasLt is used
            choices.insert(
                0,
                aten_bias_addmm.bind(
                    (inp_expanded, mat1, mat2), layout, alpha=alpha, beta=beta
                ),
            )

    return autotune_select_algorithm(
        "addmm", choices, [inp_expanded, mat1, mat2], layout
    )
