def launch(args):
    if args.no_python and not args.use_env:
        raise ValueError(
            "When using the '--no_python' flag,"
            " you must also set the '--use_env' flag."
        )
    run(args)
