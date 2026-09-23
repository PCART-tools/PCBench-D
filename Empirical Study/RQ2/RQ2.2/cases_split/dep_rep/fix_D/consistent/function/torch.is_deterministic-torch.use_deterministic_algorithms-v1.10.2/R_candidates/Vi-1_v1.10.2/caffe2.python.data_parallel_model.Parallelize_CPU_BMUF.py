def Parallelize_CPU_BMUF(*args, **kwargs):
    kwargs['cpu_device'] = True
    Parallelize_BMUF(*args, **kwargs)
