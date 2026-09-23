def construct_adder(n: int, dtype=torch.float32):
    A = te.BufHandle("A", [n], dtype)
    B = te.BufHandle("B", [n], dtype)

    def compute(i):
        return A.load([i]) + B.load([i])

    C = te.Compute("C", [n], compute)

    loopnest = te.LoopNest([C])
    loopnest.prepare_for_codegen()
    stmt = te.simplify(loopnest.root_stmt())

    return te.construct_codegen("ir_eval", stmt, [A, B, C])
