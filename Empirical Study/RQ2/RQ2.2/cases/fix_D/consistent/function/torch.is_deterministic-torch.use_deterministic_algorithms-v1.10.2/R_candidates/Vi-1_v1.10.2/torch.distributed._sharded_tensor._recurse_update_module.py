def _recurse_update_module(module, state_dict, prefix):
    for attr_name, attr in module.__dict__.items():
        key = prefix + attr_name
        if key in state_dict:
            if isinstance(state_dict[key], ShardedTensor):
                setattr(module, attr_name, state_dict[key])

    for submodule_name, submodule in module.named_modules():
        key = prefix + submodule_name
        if submodule_name:
            _recurse_update_module(submodule, state_dict, key + '.')
