def apply_assignments(net, blob_assignments):
    def canonical_name(blob):
        if blob not in blob_assignments:
            return blob
        return blob_assignments[blob]

    for op in net.op:
        # Descend into subnets of the recurrent network
        if op.type.startswith('RecurrentNetwork'):
            apply_recurrent_blob_assignments(op, blob_assignments, canonical_name)

        for i, input_ in enumerate(op.input):
            op.input[i] = canonical_name(input_)
        for i, output in enumerate(op.output):
            op.output[i] = canonical_name(output)
