def add_tensor(net, name, blob):
    ''' Create an operator to store the tensor 'blob',
        run the operator to put the blob to workspace.
        uint8 is stored as an array of string with one element.
    '''
    kTypeNameMapper = {
        np.dtype('float32'): "GivenTensorFill",
        np.dtype('int32'): "GivenTensorIntFill",
        np.dtype('int64'): "GivenTensorInt64Fill",
        np.dtype('uint8'): "GivenTensorStringFill",
    }

    shape = blob.shape
    values = blob
    # pass array of uint8 as a string to save storage
    # storing uint8_t has a large overhead for now
    if blob.dtype == np.dtype('uint8'):
        shape = [1]
        values = [str(blob.data)]

    op = core.CreateOperator(
        kTypeNameMapper[blob.dtype],
        [], [name],
        arg=[
            utils.MakeArgument("shape", shape),
            utils.MakeArgument("values", values),
        ]
    )
    net.op.extend([op])
