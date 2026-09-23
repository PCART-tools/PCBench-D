def Parallelize_GPU_BMUF(*args, **kwargs):
    kwargs['cpu_device'] = False
    Parallelize_BMUF(*args, **kwargs)
