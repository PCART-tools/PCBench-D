def blob_uses(net, blob):
    u = []
    for i, op in enumerate(net.op):
        if blob in op.input or blob in op.control_input:
            u.append(i)
    return u
