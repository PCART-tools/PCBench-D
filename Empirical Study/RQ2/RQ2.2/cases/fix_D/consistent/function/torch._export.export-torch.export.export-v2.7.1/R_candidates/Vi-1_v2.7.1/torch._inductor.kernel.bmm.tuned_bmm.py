@L.register_lowering(aten.bmm)
def tuned_bmm(mat1, mat2, *, layout=None):
    if all(x.get_device().type == "cpu" for x in [mat1, mat2]):
        # decompose to small ops when memory bound
        if mat1.get_size()[1] == 1 or mat2.get_size()[2] == 1:
            mat1 = L.unsqueeze(mat1, -1)
            mat2 = L.unsqueeze(mat2, 1)
            return L.sum_(L.mul(mat1, mat2), axis=2)

        def is_valid_to_require_contiguous(t):
            if not ir.is_storage_and_layout(t):
                return True
            _, layout = ir.as_storage_and_layout(t, freeze=False)
            return isinstance(layout, ir.FlexibleLayout)

        def is_preferred_layout_as_bmm_input(sizes, strides):
            # contiguous on one of the last two dims
            return (
                strides[-1] == 1 and (sizes[-2] == 1 or strides[-2] >= sizes[-1])
            ) or (strides[-2] == 1 and (sizes[-1] == 1 or strides[-1] >= sizes[-2]))

        # Make the input of bmm contiguous
        # if it is not contiguous on either of the last two dims,
        # because bmm cpu implementation would do contiguous() if not.
        # This is to avoid additional copies in bmm.
        def may_require_contiguous(t, meta_t):
            sizes = meta_t.meta["val"].size()
            strides = meta_t.meta["val"].stride()
            if not is_preferred_layout_as_bmm_input(sizes, strides):
                t = ir.ExternKernel.require_contiguous(t)
            return t

        if is_valid_to_require_contiguous(mat1):
            meta_mat1 = V.graph.current_node.args[0]
            mat1 = may_require_contiguous(mat1, meta_mat1)
        if is_valid_to_require_contiguous(mat2):
            meta_mat2 = V.graph.current_node.args[1]
            mat2 = may_require_contiguous(mat2, meta_mat2)

    m, n, k, layout, mat1, mat2 = mm_args(mat1, mat2, layout=layout)

    # below is for getting an overview logging info of inductor mms
    counters["aten_mm_info"][f"aten.bmm_{m}_{n}_{k}"] += 1
    log.info(
        "Tuned aten.bmm: m=%s, n=%s, k=%s, mat1_dtype=%s, mat2_dtype=%s, output_layout=%s",
        m,
        n,
        k,
        mat1.get_dtype(),
        mat2.get_dtype(),
        layout,
    )

    # options to tune from
    choices = [aten_bmm.bind((mat1, mat2), layout)] if use_aten_gemm_kernels() else []
    if use_triton_template(layout):
        for config in bmm_configs(m, n, k, device_type=ir.get_device_type(mat1)):
            bmm_template.maybe_append_choice(
                choices,
                input_nodes=(mat1, mat2),
                layout=layout,
                **mm_options(config, m, n, k, layout),
            )
    static_shape, is_nonzero = _is_static_problem(layout)
    if static_shape and is_nonzero and use_cutlass_template(layout, m, n, k):
        from ..codegen.cuda.gemm_template import CUTLASS3xGemmTemplate

        CUTLASS3xGemmTemplate.add_cutlass_gemm_choices(choices, layout, [mat1, mat2])

    if use_cpp_bmm_template(layout, mat1, mat2):
        from ..codegen.cpp_bmm_template import CppBmmTemplate

        CppBmmTemplate.add_choices(
            choices,
            layout,
            [mat1, mat2],
        )

    if use_ck_gemm_template(layout, m, n, k):
        CKGemmTemplate.add_ck_gemm_choices(choices, layout, [mat1, mat2])

    if should_fallback_to_aten(choices):
        choices.append(aten_bmm.bind((mat1, mat2), layout))

    return autotune_select_algorithm("bmm", choices, [mat1, mat2], layout)
