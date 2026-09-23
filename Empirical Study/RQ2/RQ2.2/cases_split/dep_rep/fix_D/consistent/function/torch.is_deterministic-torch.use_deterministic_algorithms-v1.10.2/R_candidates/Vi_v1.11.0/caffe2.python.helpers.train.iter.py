def iter(model, blob_out, **kwargs):
    if 'device_option' in kwargs:
        del kwargs['device_option']
    model.param_init_net.ConstantFill(
        [],
        blob_out,
        shape=[1],
        value=0,
        dtype=core.DataType.INT64,
        device_option=core.DeviceOption(caffe2_pb2.CPU, 0),
        **kwargs
    )
    return model.net.Iter(blob_out, blob_out, **kwargs)
