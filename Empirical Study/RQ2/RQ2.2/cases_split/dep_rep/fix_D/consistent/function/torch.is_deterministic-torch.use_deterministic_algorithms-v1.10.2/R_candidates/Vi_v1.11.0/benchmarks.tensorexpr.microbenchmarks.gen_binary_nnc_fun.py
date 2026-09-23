def gen_binary_nnc_fun(fn):
    def nnc_fun(A, B):
        def compute(i, j):
            return fn(A.load([i, j]), B.load([i, j]))
        return compute
    return nnc_fun
