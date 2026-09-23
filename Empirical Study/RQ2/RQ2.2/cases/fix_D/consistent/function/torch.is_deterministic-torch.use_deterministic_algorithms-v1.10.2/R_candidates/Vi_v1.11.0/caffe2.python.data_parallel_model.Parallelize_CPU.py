def Parallelize_CPU(*args, **kwargs):
    kwargs['cpu_device'] = True
    Parallelize(*args, **kwargs)
