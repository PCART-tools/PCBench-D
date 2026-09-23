def repro_run(options, exported_program, config_patches):
    from torch._inductor import _aoti_compile_and_package_inner

    gm, args, kwargs = repro_common(options, exported_program)

    from torch.cuda import synchronize

    _aoti_compile_and_package_inner(
        gm,
        args,
        kwargs,
        load_and_run=True,
        check_accuracy=options.accuracy,
        inductor_configs=config_patches,
    )

    need_sync = False

    for arg in args:
        if isinstance(arg, torch.Tensor) and arg.is_cuda:
            need_sync = True
            break

    if need_sync:
        synchronize()  # ensure segfaults are surfaced
