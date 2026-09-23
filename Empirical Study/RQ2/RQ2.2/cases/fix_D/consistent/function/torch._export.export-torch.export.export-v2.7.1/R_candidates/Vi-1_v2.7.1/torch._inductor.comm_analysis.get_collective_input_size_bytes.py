def get_collective_input_size_bytes(node: ir.IRNode) -> int:
    sz_bytes = 0
    for inp in node.inputs:  # type: ignore[attr-defined]
        numel = sympy_product(inp.layout.size)
        if isinstance(numel, sympy.Integer):
            # For ease of testing
            numel = int(numel)
        else:
            numel = V.graph.sizevars.size_hint(numel, fallback=0)
        sz_bytes += numel * get_dtype_size(inp.layout.dtype)
    return sz_bytes
