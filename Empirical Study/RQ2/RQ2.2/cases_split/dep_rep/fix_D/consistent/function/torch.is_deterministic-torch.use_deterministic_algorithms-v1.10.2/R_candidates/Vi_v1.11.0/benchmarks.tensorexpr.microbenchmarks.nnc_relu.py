def nnc_relu(A, B):
    def f(i, j):
        return torch._C._te.ifThenElse(A.load([i, j]) < torch._C._te.ExprHandle.float(0),
                                       torch._C._te.ExprHandle.float(0), A.load([i, j]))
    return f
