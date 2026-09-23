def _IsIDEEPBlob(model, blob_name):
    if blob_name in model._blob_to_device:
        return model._blob_to_device[blob_name].device_type == caffe2_pb2.IDEEP
    else:
        blob_name = "{}_{}/{}".format(
            model._device_prefix, model._devices[0], blob_name
        )
        if blob_name not in model._blob_to_device:
            return model._device_type == caffe2_pb2.IDEEP
        return model._blob_to_device[blob_name].device_type == caffe2_pb2.IDEEP
