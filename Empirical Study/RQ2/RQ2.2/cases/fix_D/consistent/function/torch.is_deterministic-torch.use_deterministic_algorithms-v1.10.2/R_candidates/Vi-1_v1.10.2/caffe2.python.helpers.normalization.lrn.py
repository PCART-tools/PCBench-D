def lrn(model, blob_in, blob_out, order="NCHW", use_cudnn=False, **kwargs):
    """LRN"""
    dev = kwargs['device_option'] if 'device_option' in kwargs \
        else scope.CurrentDeviceScope()
    is_cpu = dev is None or dev.device_type == caffe2_pb2.CPU
    if use_cudnn and (not is_cpu):
        kwargs['engine'] = 'CUDNN'
        blobs_out = blob_out
    else:
        blobs_out = [blob_out, "_" + blob_out + "_scale"]
    lrn = model.net.LRN(
        blob_in,
        blobs_out,
        order=order,
        **kwargs
    )

    if use_cudnn and (not is_cpu):
        return lrn
    else:
        return lrn[0]
