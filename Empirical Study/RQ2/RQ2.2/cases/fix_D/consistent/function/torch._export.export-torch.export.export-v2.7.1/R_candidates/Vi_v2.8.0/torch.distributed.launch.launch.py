def launch(args):
    if args.no_python and not args.use_env:
        raise ValueError(
            "When using the '--no-python' flag, you must also set the '--use-env' flag."
        )
    run(args)
