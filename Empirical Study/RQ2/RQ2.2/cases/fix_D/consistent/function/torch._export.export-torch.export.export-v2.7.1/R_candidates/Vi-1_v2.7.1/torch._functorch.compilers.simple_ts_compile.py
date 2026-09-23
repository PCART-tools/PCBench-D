@make_boxed_compiler
def simple_ts_compile(fx_g, _):
    strip_overloads(fx_g)
    f = torch.jit.script(fx_g)
    f = torch.jit.freeze(f.eval())
    return f
