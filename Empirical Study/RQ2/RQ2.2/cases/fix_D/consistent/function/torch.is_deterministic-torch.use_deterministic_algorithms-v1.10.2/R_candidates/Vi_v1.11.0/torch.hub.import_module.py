def import_module(name, path):
    warnings.warn('The use of torch.hub.import_module is deprecated in v0.11 and will be removed in v0.12', DeprecationWarning)
    return _import_module(name, path)
