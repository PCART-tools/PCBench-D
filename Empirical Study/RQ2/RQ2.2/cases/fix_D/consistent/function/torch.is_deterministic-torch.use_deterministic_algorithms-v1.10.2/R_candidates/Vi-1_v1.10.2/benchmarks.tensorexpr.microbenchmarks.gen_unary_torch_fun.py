def gen_unary_torch_fun(torch_op):
    def torch_fun(a, b, out):
        def fun():
            return torch_op(a, out=out)
        return fun
    return torch_fun
