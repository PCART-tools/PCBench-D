def verify_inplace_blobs(net_a, net_b):
    """
    Verifies that net_a and net_b have the same in-place blob assignments.
    Particularly, that memonger did not add an in-place assignment when that
    did not exist before.
    """
    def get_inplaces(op):
        out = list(op.output)
        inplaces = []
        for j, inp in enumerate(op.input):
            if inp in out:
                inplaces.append([j, out.index(inp)])
        return inplaces

    for op_a, op_b in zip(net_a.op, net_b.op):
        if op_a.type != op_b.type:
            return False
        if get_inplaces(op_a) != get_inplaces(op_b):
            return False
    return True
