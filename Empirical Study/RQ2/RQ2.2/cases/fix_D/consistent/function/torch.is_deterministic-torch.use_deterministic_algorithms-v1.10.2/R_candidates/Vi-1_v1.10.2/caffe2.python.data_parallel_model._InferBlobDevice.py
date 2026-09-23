def _InferBlobDevice(model):
    '''
    Assign blob to device option based on the operator outputing it
    '''
    mapping = {}

    def map_ops(proto):
        for op in proto.op:
            device_option = op.device_option
            if op.type == "Iter":
                # Hack for Iters which have blob in CPU context
                device_option = caffe2_pb2.DeviceOption()
                device_option.device_type = caffe2_pb2.CPU
            for b in list(op.input) + list(op.output):
                if b not in mapping:
                    mapping[b] = device_option
            if op.type.startswith('RecurrentNetwork'):
                step_args = [a for a in op.arg if a.name.endswith("step_net")]
                for step_arg in step_args:
                    map_ops(step_arg.n)
    map_ops(model.param_init_net.Proto())
    map_ops(model.net.Proto())
    model._blob_to_device = mapping
