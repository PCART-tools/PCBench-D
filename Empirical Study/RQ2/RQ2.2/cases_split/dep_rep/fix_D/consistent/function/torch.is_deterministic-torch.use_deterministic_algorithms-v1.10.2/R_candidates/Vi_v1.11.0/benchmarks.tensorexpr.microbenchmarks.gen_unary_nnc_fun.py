def gen_unary_nnc_fun(nnc_name):
    def nnc_fun(A, B):
        def compute(i, j):
            return getattr(A.load([i, j]), nnc_name)()
        return compute
    return nnc_fun
