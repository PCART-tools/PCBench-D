def gen_binary_torch_fun(fn):
    def pt_fun(a, b, out):
        def fun():
            return fn(a, b, out=out)
        return fun
    return pt_fun
