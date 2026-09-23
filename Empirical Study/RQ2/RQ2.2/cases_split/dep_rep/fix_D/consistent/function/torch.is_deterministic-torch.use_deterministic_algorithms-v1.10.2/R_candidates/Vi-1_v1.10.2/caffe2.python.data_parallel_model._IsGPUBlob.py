def _IsGPUBlob(model, blob_name):
    if blob_name in model._blob_to_device:
        return core.IsGPUDeviceType(model._blob_to_device[blob_name].device_type)
    else:
        blob_name = "{}_{}/{}".format(
            model._device_prefix, model._devices[0], blob_name
        )
        if blob_name not in model._blob_to_device:
            return core.IsGPUDeviceType(model._device_type)
        return core.IsGPUDeviceType(model._blob_to_device[blob_name].device_type)
