def GetGPUMemoryUsageStats():
    """Get GPU memory usage stats from CUDAContext/HIPContext. This requires flag
       --caffe2_gpu_memory_tracking to be enabled"""
    from caffe2.python import workspace, core
    workspace.RunOperatorOnce(
        core.CreateOperator(
            "GetGPUMemoryUsage",
            [],
            ["____mem____"],
            device_option=core.DeviceOption(workspace.GpuDeviceType, 0),
        ),
    )
    b = workspace.FetchBlob("____mem____")
    return {
        'total_by_gpu': b[0, :],
        'max_by_gpu': b[1, :],
        'total': np.sum(b[0, :]),
        'max_total': np.sum(b[1, :])
    }
