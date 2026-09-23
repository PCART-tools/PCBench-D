def _Workspace_feed_blob(ws, name, arr, device_option=None):
    if type(arr) is caffe2_pb2.TensorProto:
        arr = utils.Caffe2TensorToNumpyArray(arr)
    if type(arr) is np.ndarray and arr.dtype.kind in 'SU':
        # Plain NumPy strings are weird, let's use objects instead
        arr = arr.astype(np.object)

    if device_option is None:
        device_option = scope.CurrentDeviceScope()

    if device_option and device_option.device_type == caffe2_pb2.CUDA:
        if arr.dtype == np.dtype('float64'):
            logger.warning(
                "CUDA operators do not support 64-bit doubles, " +
                "please use arr.astype(np.float32) or np.int32 for ints." +
                " Blob: {}".format(name) +
                " type: {}".format(str(arr.dtype))
            )

    name = StringifyBlobName(name)
    if device_option is not None:
        return ws.create_blob(name).feed(arr, device_option)
    else:
        return ws.create_blob(name).feed(arr)
