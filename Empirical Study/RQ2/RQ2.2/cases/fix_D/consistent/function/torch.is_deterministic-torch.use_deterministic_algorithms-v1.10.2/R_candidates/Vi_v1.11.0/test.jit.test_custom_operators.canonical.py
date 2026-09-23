def canonical(graph):
    return torch._C._jit_pass_canonicalize(graph).str(False)
