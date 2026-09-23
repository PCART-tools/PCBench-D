def estimate_memory_usage(protos, shapes, types, devicescope):
    import numpy as np
    '''
    Estimate memory usage of a model. This is an estimate because
    we assume a single threaded execution and miss some internal
    memory usage of operators. Only estimates the memory for a given
    device scope.

    Also, currently it does not handle correctly if blob sizes vary
    during execution, as it uses only the final blob size.

    Returns (total, highwater, by op type) memory allocation in bytes.
    '''
    sizeofs = {
        caffe2_pb2.TensorProto.DOUBLE: 8,
        caffe2_pb2.TensorProto.FLOAT: 4,
        caffe2_pb2.TensorProto.FLOAT16: 2,
        caffe2_pb2.TensorProto.INT32: 4,
        caffe2_pb2.TensorProto.INT8: 1,
        caffe2_pb2.TensorProto.UINT8: 1,
        caffe2_pb2.TensorProto.UINT16: 2,
        caffe2_pb2.TensorProto.INT16: 2,
        caffe2_pb2.TensorProto.BOOL: 1,
        caffe2_pb2.TensorProto.INT64: 8,
    }

    def split_net(proto):
        ops = [op for op in proto.op if
               op.device_option == devicescope or op.type in {"Free", "Alias"}]
        del proto.op[:]
        proto.op.extend(ops)
        return proto

    def num_bytes(blob):
        if blob not in shapes or blob not in types:
            log.warning("Unknown blob encountered: {}".format(blob))
            return 0
        sizeof = sizeofs[types[blob]]
        return sizeof * np.prod(shapes[blob])

    protos = [split_net(proto) for proto in protos]
    allocs_by_ops = collections.defaultdict(lambda: 0)

    # Evaluate
    current_allocated = 0
    max_allocated = 0
    total_allocated = 0
    allocated = set()
    for proto in protos:
        for op in proto.op:
            if op.type == "Free" or op.type == "Alias":
                for o in op.output:
                    if o in allocated:
                        current_allocated -= num_bytes(o)
                        allocated.remove(o)
            else:
                for output in op.output:
                    if output not in allocated:
                        nbytes = num_bytes(output)
                        total_allocated += nbytes
                        current_allocated += nbytes
                        max_allocated = max(max_allocated, current_allocated)
                        allocated.add(output)
                        allocs_by_ops[op.type] += nbytes

    return (total_allocated, max_allocated, allocs_by_ops)
