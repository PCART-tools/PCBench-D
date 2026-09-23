def _is_from_torch(obj: Any) -> bool:
    module_name = getattr(obj, '__module__', None)
    if module_name is not None:
        base_module = module_name.partition('.')[0]
        return base_module == 'torch'

    name = getattr(obj, '__name__', None)
    # exclude torch because torch.torch.torch.torch works. idk mang
    if name is not None and name != 'torch':
        for guess in [torch, torch.nn.functional]:
            if getattr(guess, name, None) is obj:
                return True

    return False
