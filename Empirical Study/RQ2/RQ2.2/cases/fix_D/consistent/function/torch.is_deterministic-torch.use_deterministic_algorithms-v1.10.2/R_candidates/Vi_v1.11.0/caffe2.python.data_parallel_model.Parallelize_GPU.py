def Parallelize_GPU(*args, **kwargs):
    kwargs['cpu_device'] = False
    Parallelize(*args, **kwargs)
