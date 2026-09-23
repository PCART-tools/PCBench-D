def repro_minify(options, mod, load_args):
    args = run_load_args(options, mod, load_args)

    # Setup debug minifier compiler
    if not options.accuracy:
        compiler_fn = lookup_backend("dynamo_minifier_backend")
    else:
        compiler_fn = lookup_backend("dynamo_accuracy_minifier_backend")

    if options.backend is None:
        raise RuntimeError(
            "Compiler name is None - this likely means that a custom compiler "
            "was called by torchdynamo. Please remove this error, import your "
            "custom compiler function, and replace the backend=None "
            "line in run_repro to backend=<my_imported_custom_function>"
        )

    dynamo_minifier_backend = functools.partial(
        compiler_fn,
        compiler_name=options.backend,
    )
    opt_mod = torch._dynamo.optimize(dynamo_minifier_backend)(mod)

    with torch.amp.autocast("cuda", enabled=options.autocast):
        opt_mod(*args)
