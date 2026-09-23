def _recurse_update_dict(module, destination, prefix):
    for attr_name, attr in module.__dict__.items():
        if isinstance(attr, ShardedTensor):
            destination[prefix + attr_name] = attr

    for submodule_name, submodule in module.named_modules():
        if submodule_name != '':
            _recurse_update_dict(submodule, destination, prefix + submodule_name + '.')
