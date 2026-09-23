def copy_func_between_devices(src, dst):
    CPU = caffe2_pb2.CPU
    is_src_gpu = IsGPUDeviceType(src.device_type)
    is_dst_gpu = IsGPUDeviceType(dst.device_type)

    if src.device_type == CPU and dst.device_type == CPU:
        return None

    if is_src_gpu and is_dst_gpu:
        if src.device_id == dst.device_id:
            return None
        else:
            def fun(net, *args, **kw):
                with DeviceScope(dst):
                    return net.Copy(*args, **kw)
            return fun

    if is_src_gpu and dst.device_type == CPU:
        def fun(net, *args, **kw):
            with DeviceScope(src):
                return net.CopyGPUToCPU(*args, **kw)
        return fun

    if src.device_type == CPU and is_dst_gpu:
        def fun(net, *args, **kw):
            with DeviceScope(dst):
                return net.CopyCPUToGPU(*args, **kw)
        return fun

    raise ValueError('Non-supported devices: %s and %s' % (src, dst))
