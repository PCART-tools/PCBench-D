@make_boxed_compiler
def print_compile(fx_g, _):
    print(fx_g.code)
    return fx_g
