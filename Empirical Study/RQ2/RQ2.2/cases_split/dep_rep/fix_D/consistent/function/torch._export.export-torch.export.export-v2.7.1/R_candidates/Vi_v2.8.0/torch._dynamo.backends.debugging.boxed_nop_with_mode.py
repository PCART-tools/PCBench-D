def boxed_nop_with_mode(fx_g, example_inputs, *, mode):
    def run(args):
        with mode:
            return torch.fx.Interpreter(fx_g).boxed_run(args)

    run._boxed_call = True
    return run
