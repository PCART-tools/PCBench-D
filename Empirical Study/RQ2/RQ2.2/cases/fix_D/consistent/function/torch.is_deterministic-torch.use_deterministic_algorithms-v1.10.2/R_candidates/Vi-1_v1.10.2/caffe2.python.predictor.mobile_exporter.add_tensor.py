def add_tensor(net, name, blob):
    ''' Create an operator to store the tensor 'blob',
        run the operator to put the blob to workspace.
        uint8 is stored as an array of string with one element.
    '''
    kTypeNameMapper = {
        np.dtype('float32'): "GivenTensorFill",
        np.dtype('int32'): "GivenTensorIntFill",
        np.dtype('int64'): "GivenTensorInt64Fill",
        np.dtype('uint8'): "GivenTensorByteStringToUInt8Fill",
        np.dtype('O'): "GivenTensorStringFill"
    }

    shape = blob.shape
    values = blob
    # pass array of uint8 as a string to save storage
    # storing uint8_t has a large overhead for now
    if blob.dtype == np.dtype('uint8'):
        shape = blob.shape
        values = [blob.tobytes()]
    # Only allow string arrays as objects.
    # The only intended use case for this is to store arrays of strings in the
    # model which can be used for post processing results in subsequent ops.
    if blob.dtype == np.dtype('O'):
        for blob_val in blob:
            assert(isinstance(blob_val, bytes))

    op = core.CreateOperator(
        kTypeNameMapper[blob.dtype],
        [], [name],
        arg=[
            utils.MakeArgument("shape", shape),
            utils.MakeArgument("values", values),
        ]
    )
    net.op.extend([op])
