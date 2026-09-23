def gen_custom_torch_fun(fn):
    def pt_fun(a, b, out):
        def fun():
            return fn(a, b, out)
        return fun
    return pt_fun
