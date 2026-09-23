@functools.cache
def dynamo_dir():
    import torch._dynamo

    return _module_dir(torch._dynamo)
