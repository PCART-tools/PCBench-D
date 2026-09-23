def nn_module_new(cls):
    obj = object_new(cls)
    torch.nn.Module.__init__(obj)
    return obj
