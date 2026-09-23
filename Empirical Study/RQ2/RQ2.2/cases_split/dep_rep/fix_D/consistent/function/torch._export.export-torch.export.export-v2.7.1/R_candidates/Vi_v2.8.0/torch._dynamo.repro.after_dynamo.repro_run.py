def repro_run(options, mod, load_args):
    opt_mod = torch._dynamo.optimize(options.backend)(mod)

    if options.accuracy != "":
        mod.eval()
        opt_mod.eval()

        with torch.amp.autocast("cuda", enabled=options.autocast):
            # TODO: disable clone
            args = run_load_args(options, mod, load_args)
            assert same_two_models(mod, mod, args), "Eager itself failed"
            if not same_two_models(
                mod,
                opt_mod,
                args,
                only_fwd=config.repro_forward_only,
                ignore_non_fp=config.repro_ignore_non_fp,
            ):
                raise AccuracyError("Dynamo failed")
    else:
        with torch.amp.autocast("cuda", enabled=options.autocast):
            args = run_load_args(options, mod, load_args)
            run_fwd_maybe_bwd(mod, args, only_fwd=options.only_fwd, disable_clone=True)
            del args

            args = run_load_args(options, mod, load_args)
            run_fwd_maybe_bwd(
                opt_mod, args, only_fwd=options.only_fwd, disable_clone=True
            )
