def tuned_mm_plus_mm(mat1, mat2, mat3, mat4, *, layout=None):
    """
    Computes mm(mat1, mat2) + mm(mat3, mat4)
    """
    m1, n1, k1, layout1, mat1, mat2 = mm_args(mat1, mat2, layout=layout)
    m2, n2, _, layout2, mat3, mat4 = mm_args(mat3, mat4, layout=layout)
    device_type = ir.get_device_type(mat1)

    # Optimization is optional, because we can always just not do the fusion
    if (
        m1 * n1 == 0
        or m2 * n2 == 0
        or not V.graph.sizevars.statically_known_list_equals(
            mat1.get_size(), mat3.get_size()
        )
        or not V.graph.sizevars.statically_known_list_equals(
            mat2.get_size(), mat4.get_size()
        )
    ):
        # TODO(jansel): support different K values when this is fixed:
        # https://github.com/triton-lang/triton/issues/967
        return lowerings[aten.add](
            lowerings[aten.mm](mat1, mat2), lowerings[aten.mm](mat3, mat4)
        )

    assert layout1 == layout2
    # options to tune from
    choices = (
        [aten_mm_plus_mm.bind((mat1, mat2, mat3, mat4), layout1)]
        if use_aten_gemm_kernels()
        else []
    )

    mm_configs = V.choices.get_mm_plus_mm_configs(device_type)
    if use_triton_template(layout1):
        for config in mm_configs():
            # see https://github.com/triton-lang/triton/issues/1298
            # BLOCK_K = K causes llvm error
            if V.graph.sizevars.statically_known_lt(config.kwargs["BLOCK_K"], k1):
                mm_plus_mm_template.maybe_append_choice(
                    choices,
                    input_nodes=(mat1, mat2, mat3, mat4),
                    layout=layout1,
                    **mm_options(config, m1, n1, k1, layout1),
                )

    return autotune_select_algorithm(
        "mm_plus_mm", choices, [mat1, mat2, mat3, mat4], layout1
    )
