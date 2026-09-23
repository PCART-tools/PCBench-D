def is_from_local(value):
    if not DistributedVariable.is_available():
        return False
    from torch.distributed.tensor import DTensor

    return inspect.isfunction(value) and value is DTensor.from_local
