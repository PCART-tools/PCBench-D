def inductor_accuracy_fails(
    fx_g, args, check_str=None, *, require_fp64=False, ignore_non_fp=False
):
    from torch._inductor.compile_fx import compile_fx_inner

    return backend_aot_accuracy_fails(
        fx_g,
        args,
        compile_fx_inner,
        require_fp64=require_fp64,
        ignore_non_fp=ignore_non_fp,
    )
