def check_module_initialized(mod):
    assert isinstance(mod, torch.nn.Module)
    if not hasattr(mod, '_parameters'):
        raise RuntimeError("'{}' has not been initialized, did you forget to call 'super()'?"
                           .format(torch.typename(type(mod))))

    # This is to avoid importing torch.distributed.nn
    if not hasattr(mod, 'remote_parameters'):
        for name, param in mod._parameters.items():
            if param is not None and torch.nn.parameter.is_lazy(param):
                raise RuntimeError("'{}' has uninitialized parameters {}. Did you forget to run a forward pass?"
                                   .format(torch.typename(type(mod)), name))
        for name, buf in mod._buffers.items():
            if buf is not None and torch.nn.parameter.is_lazy(buf):
                raise RuntimeError("'{}' has uninitialized buffers {}. Did you forget to run a forward pass?"
                                   .format(torch.typename(type(mod)), name))
