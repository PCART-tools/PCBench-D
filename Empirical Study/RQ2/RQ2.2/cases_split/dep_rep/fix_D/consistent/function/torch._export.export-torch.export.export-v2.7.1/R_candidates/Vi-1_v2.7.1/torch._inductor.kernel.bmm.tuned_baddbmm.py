@L.register_lowering(aten.baddbmm)
def tuned_baddbmm(inp, mat1, mat2, *, alpha=1, beta=1, layout=None):
    m, n, k, layout, mat1, mat2, inp = mm_args(mat1, mat2, inp, layout=layout)

    # below is for getting an overview logging info of inductor mms
    counters["aten_mm_info"][f"aten.baddbmm_{m}_{n}_{k}"] += 1
    log.info(
        "Tuned aten.baddbmm: m=%s, n=%s, k=%s, mat1_dtype=%s, mat2_dtype=%s, inp=%s, output_layout=%s",
        m,
        n,
        k,
        mat1.get_dtype(),
        mat2.get_dtype(),
        inp.get_dtype(),
        layout,
    )

    # options to tune from
    choices = (
        [aten_baddbmm.bind((inp, mat1, mat2), layout, alpha=alpha, beta=beta)]
        if use_aten_gemm_kernels()
        else []
    )
    if use_triton_template(layout):
        for config in bmm_configs(m, n, k, device_type=ir.get_device_type(mat1)):
            bmm_template.maybe_append_choice(
                choices,
                input_nodes=(inp, mat1, mat2),
                layout=layout,
                **mm_options(config, m, n, k, layout),
                prefix_args=1,
                epilogue_fn=addmm_epilogue(layout.dtype, alpha, beta),
            )

    return autotune_select_algorithm("baddbmm", choices, [inp, mat1, mat2], layout)
