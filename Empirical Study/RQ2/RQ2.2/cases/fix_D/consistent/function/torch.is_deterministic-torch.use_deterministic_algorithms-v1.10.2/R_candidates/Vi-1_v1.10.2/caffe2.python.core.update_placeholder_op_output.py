def update_placeholder_op_output(op, blob_to_device):
    '''
    Placeholder ops (for e.g. Recv) always runs on CPU. So ensure their
    output blobs reside on CPU.
    '''
    outputs = []
    for output in op.output:
        if (output in blob_to_device and
                blob_to_device[output].device_type != caffe2_pb2.CPU):
            output += '_cpu'
        outputs.append(output)
    del op.output[:]
    op.output.extend(outputs)
