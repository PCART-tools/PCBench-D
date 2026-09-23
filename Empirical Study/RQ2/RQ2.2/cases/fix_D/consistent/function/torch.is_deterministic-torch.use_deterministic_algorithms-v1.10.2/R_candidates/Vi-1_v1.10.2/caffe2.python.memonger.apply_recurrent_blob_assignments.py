def apply_recurrent_blob_assignments(op, blob_assignments, canonical_name):
    log.debug("Applying assignments to recurrent op: {}".format(op.type))
    step_args = [a for a in op.arg if a.name.endswith("step_net")]
    for step_arg in step_args:
        apply_assignments(step_arg.n, blob_assignments)
        for i, einp in enumerate(step_arg.n.external_input):
            if einp in blob_assignments:
                step_arg.n.external_input[i] = canonical_name(einp)
    # Store renamings
    for blob, renamed in viewitems(blob_assignments):
        if blob in list(op.input) + list(op.output):
            a = caffe2_pb2.Argument()
            a.name = blob + ".rename"
            a.s = str(renamed).encode("ascii")
            op.arg.extend([a])
