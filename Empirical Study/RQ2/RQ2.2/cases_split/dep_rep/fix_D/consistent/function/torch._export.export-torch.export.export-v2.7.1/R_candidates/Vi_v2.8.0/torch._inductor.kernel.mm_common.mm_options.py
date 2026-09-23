def mm_options(config, sym_m, sym_n, sym_k, layout):
    """
    Common options to matmul triton templates.
    """
    even_k_symbolic = (
        # it isn't worth guarding on this
        sympy.gcd(sym_k, config.kwargs["BLOCK_K"]) == config.kwargs["BLOCK_K"]
    )
    allow_tf32 = torch.backends.cuda.matmul.allow_tf32 and (
        not inductor_config.force_same_precision
        or ((sym_m % 16) == 0 and (sym_n % 16) == 0 and (sym_k % 8) == 0)
    )
    options_dict = dict(
        EVEN_K=even_k_symbolic,
        ALLOW_TF32=allow_tf32,
        USE_FAST_ACCUM=False,  # Option for _scaled_mm
        ACC_TYPE=acc_type(layout.dtype),
        num_stages=config.num_stages,
        num_warps=config.num_warps,
        **config.kwargs,
    )

    # If GROUP_M not specified then default to 8
    if "GROUP_M" not in config.kwargs:
        group_m = config.kwargs.get("GROUP_M", 8)
        options_dict["GROUP_M"] = group_m

    return options_dict
