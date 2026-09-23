def GetLearningRateBlobNames(model):
    '''
    Returns a list of learning rates blob names used in the optimizer.
    '''
    if model._optimizer is not None:
        if model._device_type == caffe2_pb2.CPU or model._device_type == caffe2_pb2.IDEEP:
            return [model._optimizer.get_cpu_blob_name('lr')]
        elif core.IsGPUDeviceType(model._device_type):
            return [model._optimizer.get_gpu_blob_name('lr', gpu, '')
                    for gpu in model._devices]
        else:
            raise Exception(
                "Unsupported device type : {}".format(model._device_type)
            )
    else:
        lr_blob_names = []
        for op in model.net.Proto().op:
            if op.type == "LearningRate":
                lr_blob_names.append(op.output(0))
        return lr_blob_names
