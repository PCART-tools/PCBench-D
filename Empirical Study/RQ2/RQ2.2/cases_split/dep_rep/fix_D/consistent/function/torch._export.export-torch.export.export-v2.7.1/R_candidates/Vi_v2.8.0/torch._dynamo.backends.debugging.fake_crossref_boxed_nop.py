def fake_crossref_boxed_nop(fx_g, example_inputs, ignore_op_fn=None):
    def run(args):
        with torch._subclasses.CrossRefFakeMode(ignore_op_fn):
            return torch.fx.Interpreter(fx_g).boxed_run(args)

    run._boxed_call = True
    return run
