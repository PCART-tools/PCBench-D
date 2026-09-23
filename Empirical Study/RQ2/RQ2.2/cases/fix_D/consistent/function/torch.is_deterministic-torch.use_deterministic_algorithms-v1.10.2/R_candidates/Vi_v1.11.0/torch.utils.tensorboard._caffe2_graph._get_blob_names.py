def _get_blob_names(ops):
    '''
    Get all the operator input and output blobs and perform dedup on their names.

    Args:
        ops: List of Caffe2 operators to extract inputs and outputs from

    Returns:
        set containing distinct inputs and outputs from 'ops'
    '''
    names = set()
    for op in ops:
        names.update(op.input)
        names.update(op.output)
    return {name: name for name in names}
