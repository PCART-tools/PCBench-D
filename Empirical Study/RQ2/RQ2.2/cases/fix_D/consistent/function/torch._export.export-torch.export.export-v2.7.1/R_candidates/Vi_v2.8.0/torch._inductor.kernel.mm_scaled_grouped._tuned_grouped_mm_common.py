def _tuned_grouped_mm_common(
    operator_name: str,
    algorithm_name: str,
    extern_kernel_choice: ExternKernelChoice,
    kernel_template: TritonTemplate,
    mat_a: TensorBox,
    mat_b: TensorBox,
    scale_a: Optional[TensorBox] = None,
    scale_b: Optional[TensorBox] = None,
    offs: Optional[TensorBox] = None,
    bias: Optional[TensorBox] = None,
    scale_result: Optional[TensorBox] = None,
    out_dtype: Optional[torch.dtype] = None,
    use_fast_accum: Optional[bool] = None,
    layout: Optional[Layout] = None,
) -> TensorBox:
    assert (scale_a is None) == (scale_b is None)
    assert scale_result is None or scale_a is not None

    m1_size, m2_size, layout, mat_a, mat_b, offs = grouped_mm_args(
        mat_a, mat_b, offs, layout=layout, out_dtype=out_dtype
    )
    counters["aten_mm_info"][operator_name] += 1
    log_message = f"Tuned {operator_name}: mat1_shape=%s, mat2_shape=%s, mat1_dtype=%s, mat2_dtype=%s, output_layout=%s"
    log.info(
        log_message,
        m1_size,
        m2_size,
        mat_a.get_dtype(),
        mat_b.get_dtype(),
        layout,
    )

    if scale_a is not None and scale_b is not None:
        check_supported_striding(mat_a, mat_b)

    # workaround for Inductor not supporting optional tensor input arguments
    input_nodes: list[Any] = [mat_a, mat_b]
    if scale_a is not None:
        input_nodes.append(realize_inputs(scale_a))
    if scale_b is not None:
        input_nodes.append(realize_inputs(scale_b))
    if offs is not None:
        input_nodes.append(realize_inputs(offs))

    if use_fast_accum is None:
        aten_choice = extern_kernel_choice.bind(
            input_nodes,
            layout,
            out_dtype=out_dtype,
        )
    else:
        aten_choice = extern_kernel_choice.bind(
            input_nodes,
            layout,
            out_dtype=out_dtype,
            use_fast_accum=use_fast_accum,
        )
    if use_fast_accum is None:
        use_fast_accum = False

    choices: list[ChoiceCaller] = []
    if use_aten_gemm_kernels():
        choices.append(aten_choice)

    _, is_nonzero = _is_static_problem(layout)

    # Checking only for the equality of corresponding dims of
    # multiplicands here, relying on meta function checks for
    # everything else.
    if is_nonzero and can_use_triton_kernel(mat_a, mat_b, offs, bias, scale_result):
        scaled = scale_a is not None
        if len(m1_size) == 2:
            if len(m2_size) == 2:
                m, k1 = m1_size
                k2, _ = m2_size
                g = offs.get_size()[0]
                V.graph.sizevars.guard_equals(k1, k2)
                a_is_2d, b_is_2d = True, True
            else:
                g1 = offs.layout.size[0]
                m, k1 = m1_size
                g2, k2, _ = m2_size
                g = V.graph.sizevars.guard_equals(g1, g2)
                V.graph.sizevars.guard_equals(k1, k2)
                a_is_2d, b_is_2d = True, False
        else:
            if len(m2_size) == 2:
                g1 = offs.layout.size[0]
                g2, m, k1 = m1_size
                k2, _ = m2_size
                g = V.graph.sizevars.guard_equals(g1, g2)
                V.graph.sizevars.guard_equals(k1, k2)
                a_is_2d, b_is_2d = False, True
            else:
                g1, m, k1 = m1_size
                g2, k2, _ = m2_size
                g = V.graph.sizevars.guard_equals(g1, g2)
                V.graph.sizevars.guard_equals(k1, k2)
                a_is_2d, b_is_2d = False, False

        triton_has_make_tensor_descriptor = hasattr(tl, "make_tensor_descriptor")
        triton_has_experimental_make_tensor_descriptor = hasattr(
            tl, "_experimental_make_tensor_descriptor"
        )
        use_tma_load = (
            triton_has_make_tensor_descriptor
            or triton_has_experimental_make_tensor_descriptor
        )
        # The make_tensor_descriptor imposes this additional limitation.
        use_tma_load = use_tma_load and (
            mat_a.get_stride()[-1] == 1 and mat_b.get_stride()[-2] == 1
        )

        kwargs = {
            "SCALED": scaled,
            "A_IS_2D": a_is_2d,
            "B_IS_2D": b_is_2d,
            "USE_FAST_ACCUM": use_fast_accum,
            "NUM_SMS": get_num_sms(),
            "USE_TMA_LOAD": use_tma_load,
            "USE_EXPERIMENTAL_MAKE_TENSOR_DESCRIPTOR": triton_has_experimental_make_tensor_descriptor,
        }

        for config in early_config_prune(g, m, grouped_mm_configs(), kwargs):
            kernel_template.maybe_append_choice(
                choices,
                input_nodes=input_nodes,
                layout=layout,
                num_stages=config.num_stages,
                num_warps=config.num_warps,
                **kwargs,
                **config.kwargs,
            )

    input_gen_fns = {
        4: lambda x: create_offsets(
            x, m1_size, m2_size, offs.get_size() if offs is not None else None
        ),
    }
    return autotune_select_algorithm(
        algorithm_name, choices, input_nodes, layout, input_gen_fns=input_gen_fns
    )
