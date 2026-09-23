def _get_ort_device_type(device_type: str):
    from onnxruntime.capi import _pybind_state as ORTC

    if device_type == "cuda":
        return ORTC.OrtDevice.cuda()
    if device_type == "cpu":
        return ORTC.OrtDevice.cpu()
    # ort pytorch device is mapped to NPU OrtDevice type
    if device_type == "maia":
        return ORTC.OrtDevice.npu()
    raise ValueError("Unsupported device type: " + device_type)
