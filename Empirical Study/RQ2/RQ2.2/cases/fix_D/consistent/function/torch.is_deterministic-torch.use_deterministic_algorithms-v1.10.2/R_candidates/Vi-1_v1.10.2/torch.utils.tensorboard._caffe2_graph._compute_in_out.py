def _compute_in_out(ops):
    '''
    Find the input, intermediate and output nodes of a set of operators.

    Args:
        ops: List of Caffe2 operators to look through

    Returns:
        input_blobs: The input nodes of the set of operators
        inter_blobs: The intermediate nodes of the set of operators
        output_blobs: The output nodes of the set of operators
    '''
    in_blobs = set()
    out_blobs = set()

    for op in ops:
        for input_blob in op.input:
            in_blobs.add(input_blob)
        for output_blob in op.output:
            out_blobs.add(output_blob)

    input_blobs = list(in_blobs.difference(out_blobs))
    output_blobs = list(out_blobs.difference(in_blobs))
    inter_blobs = {b for b in output_blobs if b.startswith('_')}
    output_blobs = [b for b in output_blobs if b not in inter_blobs]

    return input_blobs, inter_blobs, output_blobs
